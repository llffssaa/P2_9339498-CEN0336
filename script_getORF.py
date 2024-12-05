#!/usr/bin/env python3

import sys
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

def find_longest_orf(seq, seq_id):
    """Encontra o ORF mais longo entre as 6 fases de leitura possíveis."""
    start_codon = "ATG"
    stop_codons = {"TAA", "TAG", "TGA"}
    orf_info = {"frame": 0, "start": 0, "end": 0, "length": 0, "orf": ""}
    
    seq_obj = Seq(seq)  # Converte para objeto Seq
    
    for frame in range(3):  # Frames 1, 2, 3
        for strand, phase in [(seq_obj, frame), (seq_obj.reverse_complement(), frame + 3)]:
            orfs = []
            start = None
            for i in range(phase, len(strand), 3):
                codon = strand[i:i+3]
                if len(codon) < 3:
                    break
                if codon == start_codon and start is None:
                    start = i
                elif codon in stop_codons and start is not None:
                    orf_seq = strand[start:i+3]
                    if len(orf_seq) % 3 == 0:
                        orfs.append((start, i+3, orf_seq))
                    start = None
            
            for start, end, orf_seq in orfs:
                orf_length = end - start
                if orf_length > orf_info["length"]:
                    orf_info.update({
                        "frame": phase + 1,
                        "start": start,
                        "end": end,
                        "length": orf_length,
                        "orf": str(orf_seq)  # Converte para string
                    })
    return orf_info

def translate_orf(orf_seq):
    """Traduz uma sequência de ORF em um peptídeo."""
    return Seq(orf_seq).translate(to_stop=True)

def main():
    if len(sys.argv) != 2:
        print("Uso: script_getORF.py <arquivo_multifasta>")
        sys.exit(1)
    
    fasta_file = sys.argv[1]
    orf_fna = "ORF.fna"
    orf_faa = "ORF.faa"
    
    orf_fna_records = []
    orf_faa_records = []

    for record in SeqIO.parse(fasta_file, "fasta"):
        seq = str(record.seq)
        orf_info = find_longest_orf(seq, record.id)
        orf_seq = orf_info["orf"]
        peptide = translate_orf(orf_seq)
        
        # Criação dos identificadores
        identifier = f"{record.id}_frame{orf_info['frame']}_{orf_info['start']}_{orf_info['end']}"
        
        # Registro fasta para ORF
        orf_fna_records.append(SeqRecord(Seq(orf_seq), id=identifier, description=""))
        
        # Registro fasta para peptídeo
        orf_faa_records.append(SeqRecord(peptide, id=identifier, description=""))
    
    # Escrever os arquivos de saída
    with open(orf_fna, "w") as fna:
        SeqIO.write(orf_fna_records, fna, "fasta")
    
    with open(orf_faa, "w") as faa:
        SeqIO.write(orf_faa_records, faa, "fasta")
    
    print("Processamento concluído!")
    print(f"Arquivos gerados: {orf_fna} e {orf_faa}")

if __name__ == "__main__":
    main()
