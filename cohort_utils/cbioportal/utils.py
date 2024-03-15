import csv

maf_columns=[
    "Hugo_Symbol",
    "Entrez_Gene_Id",
    "Center",
    "NCBI_Build",
    "Chromosome",
    "Start_Position",
    "End_Position",
    "Strand",
    "Variant_Classification",
    "Variant_Type",
    "Reference_Allele",
    "Tumor_Seq_Allele1",
    "Tumor_Seq_Allele2",
    "dbSNP_RS",
    "dbSNP_Val_Status",
    "Tumor_Sample_Barcode",
    "Matched_Norm_Sample_Barcode",
    "Match_Norm_Seq_Allele1",
    "Match_Norm_Seq_Allele2",
    "Tumor_Validation_Allele1",
    "Tumor_Validation_Allele2",
    "Match_Norm_Validation_Allele1",
    "Match_Norm_Validation_Allele2",
    "Verification_Status",
    "Validation_Status",
    "Mutation_Status",
    "Sequencing_Phase",
    "Sequence_Source",
    "Validation_Method",
    "Score",
    "BAM_File",
    "Sequencer",
    "HGVSp_Short",
    "t_alt_count",
    "t_ref_count",
    "n_alt_count",
    "n_ref_count",
]

minimal_maf_columns = [
    "Chromosome",
    "Start_Position",
    "End_Position",
    "Reference_Allele",
    "Tumor_Seq_Allele1",
    "Tumor_Seq_Allele2",
]

csv.register_dialect('maf', delimiter="\t", quoting=csv.QUOTE_NONE)

def read_maf(path):
    maf_data = []
    with open(path, 'r') as f:
        reader = csv.reader(f, dialect='maf')
        for r in reader:
            maf_data.append(r)
    return maf_data

def filter_data_maf_columns(maf_data,maf_columns=maf_columns):
    header = maf_data[0]
    keep_col = [ True if i in maf_columns else False for i in header ]
    filtered_maf_data = [ [ r[i] for i in range(len(keep_col)) if keep_col[i] ] for r in maf_data ]
    return filtered_maf_data
