from cohort_utils.pb import tempo_maf_pb2
import os, shutil
from . import utils
import pandas as pd

def safe_float(value, default=-1.0):
    try:
        # If value is None, or pandas recognizes it as null,
        # or it is an empty/whitespace string, return default.
        if value is None or pd.isnull(value) or str(value).strip() == "":
            return default
        return float(value)
    except (ValueError, TypeError):
        return default

def safe_int(value, default=-1):
    try:
        if value is None or pd.isnull(value) or str(value).strip() == "":
            return default
        # Sometimes values come as strings that are floats (e.g. "5.0")
        return int(float(value))
    except (ValueError, TypeError):
        return default

class SampleProtobuf_Handler:
    def __init__(self, **kwargs):
        # Read MAF either from an already-loaded DataFrame or from file
        if "maf_table" in kwargs:
            self.maf_table = kwargs.pop("maf_table")
        else:
            self.maf_table = utils.read_maf(kwargs.pop("maf"))

        # Replace all NA/NaN values with empty strings across every column.
        self.maf_table = self.maf_table.fillna("")

        self.cmoSampleId, self.normalCmoSampleId = utils.get_sample_id_from_maf(self.maf_table)

    def generate_tempomessage(self):
        print("Generating Tempo MEssage")
        #sys.exit()
        tm = tempo_maf_pb2.TempoMessage()
        tm.cmoSampleId = self.cmoSampleId
        tm.normalCmoSampleId = self.normalCmoSampleId
        tm.pipelineVersion = "v1.0"
        tm.genomeNexusServerVersion = "server_version"
        tm.genomeNexusDatabaseVersion = "database_version"
        tm.vepVersion = "vep_version"
        tm.polyphenVersion = "polyphen_version"
        tm.siftVersion = "sift_version"
        tm.oncokbDataVersion = "oncokb_version"
        tm.oncotreeCode = "oncotree_code"
        
        for index, row in self.maf_table.iterrows():
            event = tm.events.add()

            event.chromosome = str(row.get("Chromosome", ""))
            event.startPosition = str(row.get("Start_Position", ""))
            event.endPosition = str(row.get("End_Position", ""))
            event.refAllele = str(row.get("Reference_Allele", ""))
            event.tumorSeqAllele1 = str(row.get("Tumor_Seq_Allele1", ""))
            event.tumorSeqAllele2 = str(row.get("Tumor_Seq_Allele2", ""))
            event.strand = str(row.get("Strand", ""))
            event.ncbiBuild = str(row.get("NCBI_Build", ""))
            event.hugoSymbol = str(row.get("Hugo_Symbol", ""))
            event.entrezGeneId = str(row.get("Entrez_Gene_Id", ""))
            event.variantClassification = str(row.get("Variant_Classification", ""))
            event.variantType = str(row.get("Variant_Type", ""))
            event.dbSNPRS1 = str(row.get("dbSNP_RS", ""))
            event.hgvsp = str(row.get("HGVSp", ""))
            event.hgvsp_short = str(row.get("HGVSp_Short", ""))
            event.hgvsc = str(row.get("HGVSc", ""))
            event.transcriptId = str(row.get("Transcript_ID", ""))
            event.refSeq = str(row.get("RefSeq", ""))
            event.center = str(row.get("Center", ""))
            event.consequence = str(row.get("Consequence", ""))
            event.dbSNPValStatus = str(row.get("dbSNP_Val_Status", ""))
            event.matchedNormalSampleBarcode = str(row.get("Matched_Norm_Sample_Barcode", ""))
            event.matchNormSeqAllele1 = str(row.get("Match_Norm_Seq_Allele1", ""))
            event.matchNormSeqAllele2 = str(row.get("Match_Norm_Seq_Allele2", ""))
            event.verificationStatus = str(row.get("Verification_Status", ""))
            event.validationStatus = str(row.get("Validation_Status", ""))
            event.mutationStatus = str(row.get("Mutation_Status", ""))
            event.sequencingPhase = str(row.get("Sequencing_Phase", ""))
            event.sequencingSource = str(row.get("Sequence_Source", ""))
            event.validationMethod = str(row.get("Validation_Method", ""))
            event.score = str(row.get("Score", ""))
            event.bamFile = str(row.get("BAM_File", ""))
            event.sequencer = str(row.get("Sequencer", ""))
            event.tRefCount = str(row.get("t_ref_count", ""))
            event.tAltCount = str(row.get("t_alt_count", ""))
            event.nRefCount = str(row.get("n_ref_count", ""))
            event.nAltCount = str(row.get("n_alt_count", ""))
            event.proteinPosition = str(row.get("Protein_position", ""))
            event.codons = str(row.get("Codons", ""))
            event.exonNumber = str(row.get("Exon_Number", ""))
            event.polyphenPrediction = str(row.get("Polyphen_Prediction", ""))
            event.polyphenScore = str(row.get("Polyphen_Score", ""))
            event.siftPrediction = str(row.get("Sift_Prediction", ""))
            event.siftScore = str(row.get("Sift_Score", ""))
            event.genomicLocationExplanation = str(row.get("GenomicLocationExplanation", ""))
            event.annotationStatus = str(row.get("AnnotationStatus", ""))
            event.oncokbAnnotated = str(row.get("oncokbAnnotated", ""))
            event.oncokbKnownGene = str(row.get("oncokbKnownGene", ""))
            event.oncokbKnownVariant = str(row.get("oncokbKnownVariant", ""))
            event.oncokbMutationEffect = str(row.get("oncokbMutationEffect", ""))
            event.oncokbMutationEffectCitations = str(row.get("oncokbMutationEffectCitations", ""))
            event.oncokbOncogenic = str(row.get("oncokbOncogenic", ""))
            event.oncokbLevel1 = str(row.get("oncokbLevel1", ""))
            event.oncokbLevel2 = str(row.get("oncokbLevel2", ""))
            event.oncokbLevel3A = str(row.get("oncokbLevel3A", ""))
            event.oncokbLevel3B = str(row.get("oncokbLevel3B", ""))
            event.oncokbLevel4 = str(row.get("oncokbLevel4", ""))
            event.oncokbLevelR1 = str(row.get("oncokbLevelR1", ""))
            event.oncokbLevelR2 = str(row.get("oncokbLevelR2", ""))
            event.oncokbHighestLevel = str(row.get("oncokbHighestLevel", ""))
            event.oncokbHighestSensitivityLevel = str(row.get("oncokbHighestSensitivityLevel", ""))
            event.oncokbHighestResistanceLevel = str(row.get("oncokbHighestResistanceLevel", ""))
            event.oncokbTxCitations = str(row.get("oncokbTxCitations", ""))
            event.oncokbLevelDx1 = str(row.get("oncokbLevelDx1", ""))
            event.oncokbLevelDx2 = str(row.get("oncokbLevelDx2", ""))
            event.oncokbLevelDx3 = str(row.get("oncokbLevelDx3", ""))
            event.oncokbHighestDxLevel = str(row.get("oncokbHighestDxLevel", ""))
            event.oncokbDxCitations = str(row.get("oncokbDxCitations", ""))
            event.oncokbLevelPx1 = str(row.get("oncokbLevelPx1", ""))
            event.oncokbLevelPx2 = str(row.get("oncokbLevelPx2", ""))
            event.oncokbLevelPx3 = str(row.get("oncokbLevelPx3", ""))
            event.oncokbHighestPxLevel = str(row.get("oncokbHighestPxLevel", ""))
            event.oncokbPxCitations = str(row.get("oncokbPxCitations", ""))
            

            # Fill nested Neoantigen message, if available
            neo = event.neoantigen
            neo.neo_maf_identifier_key = str(row.get("neo_maf_identifier_key", ""))
            neo.neo_best_icore_peptide = str(row.get("neo_best_icore_peptide", ""))
            neo.neo_best_rank = safe_float(row.get("neo_best_rank", ""))
            neo.neo_best_binding_affinity = safe_float(row.get("neo_best_binding_affinity", ""))
            neo.neo_best_binder_class = str(row.get("neo_best_binder_class", ""))
            neo.neo_best_is_in_wt_peptidome = (str(row.get("neo_best_is_in_wt_peptidome", "")).lower() == "true")
            neo.neo_best_algorithm = str(row.get("neo_best_algorithm", ""))
            neo.neo_best_hla_allele = str(row.get("neo_best_hla_allele", ""))
            neo.neo_n_peptides_evaluated = safe_int(row.get("neo_n_peptides_evaluated", ""))
            neo.neo_n_strong_binders = safe_int(row.get("neo_n_strong_binders", ""))
            neo.neo_n_weak_binders = safe_int(row.get("neo_n_weak_binders", ""))

            # Placeholder for FACETS stuff.
            '''
            facets = event.facets
            facets.tcn = safe_int(row.get("tcn", ""))
            facets.lcn = safe_int(row.get("lcn", ""))
            facets.cf = safe_float(row.get("cf", ""))
            facets.purity = safe_float(row.get("purity", ""))
            facets.expected_alt_copies = safe_int(row.get("expected_alt_copies", ""))
            facets.ccf_expected_copies = safe_float(row.get("ccf_expected_copies", ""))
            facets.ccf_expected_copies_lower = safe_float(row.get("ccf_expected_copies_lower", ""))
            facets.ccf_expected_copies_upper = safe_float(row.get("ccf_expected_copies_upper", ""))
            facets.ccf_expected_copies_prob95 = safe_float(row.get("ccf_expected_copies_prob95", ""))
            facets.ccf_expected_copies_prob90 = safe_float(row.get("ccf_expected_copies_prob90", ""))
            facets.clonality = str(row.get("clonality", ""))
            '''

            # Fill nested GetBaseCountsMultiSample message, if available
            base = event.getbasecountsmultisample
            base.t_alt_count_raw = safe_int(row.get("t_alt_count_raw", ""))
            base.n_alt_count_raw = safe_int(row.get("n_alt_count_raw", ""))
            base.t_alt_count_raw_fwd = safe_int(row.get("t_alt_count_raw_fwd", ""))
            base.n_alt_count_raw_fwd = safe_int(row.get("n_alt_count_raw_fwd", ""))
            base.t_alt_count_raw_rev = safe_int(row.get("t_alt_count_raw_rev", ""))
            base.n_alt_count_raw_rev = safe_int(row.get("n_alt_count_raw_rev", ""))
            base.t_ref_count_raw = safe_int(row.get("t_ref_count_raw", ""))
            base.n_ref_count_raw = safe_int(row.get("n_ref_count_raw", ""))
            base.t_ref_count_raw_fwd = safe_int(row.get("t_ref_count_raw_fwd", ""))
            base.n_ref_count_raw_fwd = safe_int(row.get("n_ref_count_raw_fwd", ""))
            base.t_ref_count_raw_rev = safe_int(row.get("t_ref_count_raw_rev", ""))
            base.n_ref_count_raw_rev = safe_int(row.get("n_ref_count_raw_rev", ""))
            base.t_depth_raw = safe_int(row.get("t_depth_raw", ""))
            base.n_depth_raw = safe_int(row.get("n_depth_raw", ""))
            base.t_depth_raw_fwd = safe_int(row.get("t_depth_raw_fwd", ""))
            base.n_depth_raw_fwd = safe_int(row.get("n_depth_raw_fwd", ""))
            base.t_depth_raw_rev = safe_int(row.get("t_depth_raw_rev", ""))
            base.n_depth_raw_rev = safe_int(row.get("n_depth_raw_rev", ""))

            # Fill nested ZygosityAnnotation message, if available
            zygo = event.zygosityannotation
            zygo.num_ref_copies = safe_int(row.get("num_ref_copies", ""))
            zygo.num_alt_copies = safe_int(row.get("num_alt_copies", ""))
            zygo.expected_t_alt_freq_lower = safe_float(row.get("expected_t_alt_freq_lower", ""))
            zygo.expected_t_alt_freq_upper = safe_float(row.get("expected_t_alt_freq_upper", ""))
            zygo.tumor_vaf_cn_concordance = (str(row.get("tumor_vaf_cn_concordance", "")).lower() == "true")
            zygo.allelic_imbalance = str(row.get("allelic_imbalance", ""))
            zygo.loss_of_heterozygosity = (str(row.get("loss_of_heterozygosity", "")).lower() == "true")
            zygo.zygosity_flag = str(row.get("zygosity_flag", ""))
        

        return tm

if __name__ == "__main__":
    # For testing purposes, pass the path to your MAF file.
    handler = SampleProtobuf_Handler(maf="./tests/data/mut_somatic.maf")
    tm = handler.generate_tempomessage()
    #print(tm)