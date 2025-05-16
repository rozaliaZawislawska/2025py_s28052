#!/usr/bin/env python3

"""
NCBI GenBank Data Retriever

Rozszerzony skrypt do łączenia się z NCBI i pobierania rekordów sekwencji genetycznych z dodatkowymi funkcjonalnościami:
- Filtrowanie długości odczytu
- Generowanie raportu CSV
- Wizualizacja danych
"""

from Bio import Entrez
from Bio import SeqIO
import time
import os
import csv
import matplotlib.pyplot as plt

class NCBIRetriever:
    def __init__(self, email, api_key):
        """Initialize with NCBI credentials."""
        self.email = email
        self.api_key = api_key
        self.filtered_records = []
        
        # Ustawienia Entrez
        Entrez.email = email
        Entrez.api_key = api_key
        Entrez.tool = 'BioScriptEx10'
       
    def search_taxid(self, taxid):
        """Search for all records associated with a taxonomic ID."""
        print(f"Searching for records with taxID: {taxid}")
        try:
            # Najpierw pobierz informacje taksonomiczne
            handle = Entrez.efetch(db="taxonomy", id=taxid, retmode="xml")
            records = Entrez.read(handle)
            organism_name = records[0]["ScientificName"]
            print(f"Organism: {organism_name} (TaxID: {taxid})")
            
            # Szukaj rekordów
            search_term = f"txid{taxid}[Organism]"
            handle = Entrez.esearch(db="nucleotide", term=search_term, usehistory="y")
            search_results = Entrez.read(handle)
            count = int(search_results["Count"])
            
            if count == 0:
                print(f"No records found for {organism_name}")
                return None
               
            print(f"Found {count} records")
            
            # Zapisz wyniki wyszukiwania do późniejszego wykorzystania
            self.webenv = search_results["WebEnv"]
            self.query_key = search_results["QueryKey"]
            self.count = count
            self.organism_name = organism_name
            
            return count
            
        except Exception as e:
            print(f"Error searching TaxID {taxid}: {e}")
            return None
            
    def fetch_records(self, start=0, max_records=10, min_length=None, max_length=None):
        """Fetch a batch of records using the stored search results with length filtering."""
        if not hasattr(self, 'webenv') or not hasattr(self, 'query_key'):
            print("No search results to fetch. Run search_taxid() first.")
            return []
            
        try:
            # Limit, aby zapobiec przeciążeniu serwera
            batch_size = min(max_records, 500)
            
            handle = Entrez.efetch(
                db="nucleotide",
                rettype="gb",
                retmode="text",
                retstart=start,
                retmax=batch_size,
                webenv=self.webenv,
                query_key=self.query_key
            )
            
            # Parsowanie rekordów GenBank
            records = list(SeqIO.parse(handle, "genbank"))
            handle.close()
            
            # Filtrowanie po długości
            filtered = []
            for record in records:
                seq_length = len(record.seq)
                if (min_length is None or seq_length >= min_length) and \
                   (max_length is None or seq_length <= max_length):
                    filtered.append({
                        'accession': record.id,
                        'length': seq_length,
                        'description': record.description
                    })
            
            self.filtered_records.extend(filtered)
            return filtered
            
        except Exception as e:
            print(f"Error fetching records: {e}")
            return []

    def generate_csv_report(self, filename="genbank_report.csv"):
        """Generate a CSV report with sequence information."""
        if not self.filtered_records:
            print("No records to generate report. Fetch records first.")
            return False
            
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['accession', 'length', 'description']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for record in self.filtered_records:
                    writer.writerow(record)
                    
            print(f"CSV report generated: {filename}")
            return True
            
        except Exception as e:
            print(f"Error generating CSV report: {e}")
            return False

    def generate_length_plot(self, filename="sequence_lengths.png"):
        """Generate a line plot of sequence lengths sorted from longest to shortest."""
        if not self.filtered_records:
            print("No records to generate plot. Fetch records first.")
            return False
            
        try:
            # Sort records by length (descending)
            sorted_records = sorted(self.filtered_records, key=lambda x: x['length'], reverse=True)
            accessions = [rec['accession'] for rec in sorted_records]
            lengths = [rec['length'] for rec in sorted_records]
            
            plt.figure(figsize=(12, 6))
            plt.plot(accessions, lengths, 'b-', marker='o')
            plt.xticks(rotation=90)
            plt.xlabel('GenBank Accession Number')
            plt.ylabel('Sequence Length (bp)')
            plt.title(f'Sequence Lengths for {self.organism_name}')
            plt.tight_layout()
            plt.savefig(filename)
            plt.close()
            
            print(f"Plot generated: {filename}")
            return True
            
        except Exception as e:
            print(f"Error generating plot: {e}")
            return False

def main():
    # Utwórz obiekt retriever
    retriever = NCBIRetriever("s28052@pjwstk.edu.pl", "7c1dd98c76b2dc4dbc72de594ab90a4a2b09")
    
    # Uzyskaj taxid od użytkownika
    taxid = input("Enter taxonomic ID (taxid) of the organism: ")
    
    # Szukaj rekordów
    count = retriever.search_taxid(taxid)
    
    if not count:
        print("No records found. Exiting.")
        return
        
    # Pobierz parametry filtrowania długości
    try:
        min_len = input("Enter minimum sequence length (leave empty for no limit): ")
        max_len = input("Enter maximum sequence length (leave empty for no limit): ")
        
        min_len = int(min_len) if min_len else None
        max_len = int(max_len) if max_len else None
    except ValueError:
        print("Invalid length values. Using no filters.")
        min_len = max_len = None
    
    # Pobierz rekordy z filtrowaniem
    print("\nFetching records with length filtering...")
    records = retriever.fetch_records(start=0, max_records=count, min_length=min_len, max_length=max_len)
    
    if not records:
        print("No records found after filtering. Exiting.")
        return
    
    # Generuj raport CSV
    csv_filename = f"taxid_{taxid}_report.csv"
    retriever.generate_csv_report(csv_filename)
    
    # Generuj wykres
    plot_filename = f"taxid_{taxid}_lengths.png"
    retriever.generate_length_plot(plot_filename)
    
    print("\nProcessing completed!")

if __name__ == "__main__":
    main()