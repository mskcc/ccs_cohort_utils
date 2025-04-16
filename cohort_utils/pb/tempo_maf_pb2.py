# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: tempo_maf.proto
# Protobuf Python Version: 6.30.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    6,
    30,
    2,
    '',
    'tempo_maf.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0ftempo_maf.proto\x12\x05tempo\"\xa4\x1a\n\x05\x45vent\x12\x12\n\nchromosome\x18\x01 \x01(\t\x12\x15\n\rstartPosition\x18\x02 \x01(\t\x12\x13\n\x0b\x65ndPosition\x18\x03 \x01(\t\x12\x11\n\trefAllele\x18\x04 \x01(\t\x12\x17\n\x0ftumorSeqAllele1\x18\x05 \x01(\t\x12\x17\n\x0ftumorSeqAllele2\x18\x06 \x01(\t\x12+\n\nneoantigen\x18\x07 \x01(\x0b\x32\x17.tempo.Event.Neoantigen\x12#\n\x06\x66\x61\x63\x65ts\x18\x08 \x01(\x0b\x32\x13.tempo.Event.Facets\x12G\n\x18getbasecountsmultisample\x18\t \x01(\x0b\x32%.tempo.Event.GetBaseCountsMultiSample\x12;\n\x12zygosityannotation\x18\n \x01(\x0b\x32\x1f.tempo.Event.ZygosityAnnotation\x12\x0e\n\x06strand\x18\x0b \x01(\t\x12\x11\n\tncbiBuild\x18\x0c \x01(\t\x12\x12\n\nhugoSymbol\x18\r \x01(\t\x12\x14\n\x0c\x65ntrezGeneId\x18\x0e \x01(\t\x12\x1d\n\x15variantClassification\x18\x0f \x01(\t\x12\x13\n\x0bvariantType\x18\x10 \x01(\t\x12\x10\n\x08\x64\x62SNPRS1\x18\x11 \x01(\t\x12\r\n\x05hgvsp\x18\x12 \x01(\t\x12\x13\n\x0bhgvsp_short\x18\x13 \x01(\t\x12\r\n\x05hgvsc\x18\x14 \x01(\t\x12\x14\n\x0ctranscriptId\x18\x15 \x01(\t\x12\x0e\n\x06refSeq\x18\x16 \x01(\t\x12\x0e\n\x06\x63\x65nter\x18\x17 \x01(\t\x12\x13\n\x0b\x63onsequence\x18\x18 \x01(\t\x12\x16\n\x0e\x64\x62SNPValStatus\x18\x19 \x01(\t\x12\"\n\x1amatchedNormalSampleBarcode\x18\x1a \x01(\t\x12\x1b\n\x13matchNormSeqAllele1\x18\x1b \x01(\t\x12\x1b\n\x13matchNormSeqAllele2\x18\x1c \x01(\t\x12\x1a\n\x12verificationStatus\x18\x1d \x01(\t\x12\x18\n\x10validationStatus\x18\x1e \x01(\t\x12\x16\n\x0emutationStatus\x18\x1f \x01(\t\x12\x17\n\x0fsequencingPhase\x18  \x01(\t\x12\x18\n\x10sequencingSource\x18! \x01(\t\x12\x18\n\x10validationMethod\x18\" \x01(\t\x12\r\n\x05score\x18# \x01(\t\x12\x0f\n\x07\x62\x61mFile\x18$ \x01(\t\x12\x11\n\tsequencer\x18% \x01(\t\x12\x11\n\ttRefCount\x18& \x01(\t\x12\x11\n\ttAltCount\x18\' \x01(\t\x12\x11\n\tnRefCount\x18( \x01(\t\x12\x11\n\tnAltCount\x18) \x01(\t\x12\x17\n\x0fproteinPosition\x18* \x01(\t\x12\x0e\n\x06\x63odons\x18+ \x01(\t\x12\x12\n\nexonNumber\x18, \x01(\t\x12\x1a\n\x12polyphenPrediction\x18- \x01(\t\x12\x15\n\rpolyphenScore\x18. \x01(\t\x12\x16\n\x0esiftPrediction\x18/ \x01(\t\x12\x11\n\tsiftScore\x18\x30 \x01(\t\x12\"\n\x1agenomicLocationExplanation\x18\x31 \x01(\t\x12\x18\n\x10\x61nnotationStatus\x18\x32 \x01(\t\x12\x17\n\x0foncokbAnnotated\x18\x33 \x01(\t\x12\x17\n\x0foncokbKnownGene\x18\x34 \x01(\t\x12\x1a\n\x12oncokbKnownVariant\x18\x35 \x01(\t\x12\x1c\n\x14oncokbMutationEffect\x18\x36 \x01(\t\x12%\n\x1doncokbMutationEffectCitations\x18\x37 \x01(\t\x12\x17\n\x0foncokbOncogenic\x18\x38 \x01(\t\x12\x14\n\x0concokbLevel1\x18\x39 \x01(\t\x12\x14\n\x0concokbLevel2\x18: \x01(\t\x12\x15\n\roncokbLevel3A\x18; \x01(\t\x12\x15\n\roncokbLevel3B\x18< \x01(\t\x12\x14\n\x0concokbLevel4\x18= \x01(\t\x12\x15\n\roncokbLevelR1\x18> \x01(\t\x12\x15\n\roncokbLevelR2\x18? \x01(\t\x12\x1a\n\x12oncokbHighestLevel\x18@ \x01(\t\x12%\n\x1doncokbHighestSensitivityLevel\x18\x41 \x01(\t\x12$\n\x1concokbHighestResistanceLevel\x18\x42 \x01(\t\x12\x19\n\x11oncokbTxCitations\x18\x43 \x01(\t\x12\x16\n\x0eoncokbLevelDx1\x18\x44 \x01(\t\x12\x16\n\x0eoncokbLevelDx2\x18\x45 \x01(\t\x12\x16\n\x0eoncokbLevelDx3\x18\x46 \x01(\t\x12\x1c\n\x14oncokbHighestDxLevel\x18G \x01(\t\x12\x19\n\x11oncokbDxCitations\x18H \x01(\t\x12\x16\n\x0eoncokbLevelPx1\x18I \x01(\t\x12\x16\n\x0eoncokbLevelPx2\x18J \x01(\t\x12\x16\n\x0eoncokbLevelPx3\x18K \x01(\t\x12\x1c\n\x14oncokbHighestPxLevel\x18L \x01(\t\x12\x19\n\x11oncokbPxCitations\x18M \x01(\t\x1a\xdf\x02\n\nNeoantigen\x12\x1e\n\x16neo_maf_identifier_key\x18\x01 \x01(\t\x12\x1e\n\x16neo_best_icore_peptide\x18\x02 \x01(\t\x12\x15\n\rneo_best_rank\x18\x03 \x01(\x01\x12!\n\x19neo_best_binding_affinity\x18\x04 \x01(\x01\x12\x1d\n\x15neo_best_binder_class\x18\x05 \x01(\t\x12#\n\x1bneo_best_is_in_wt_peptidome\x18\x06 \x01(\x08\x12\x1a\n\x12neo_best_algorithm\x18\x07 \x01(\t\x12\x1b\n\x13neo_best_hla_allele\x18\x08 \x01(\t\x12 \n\x18neo_n_peptides_evaluated\x18\t \x01(\x05\x12\x1c\n\x14neo_n_strong_binders\x18\n \x01(\x05\x12\x1a\n\x12neo_n_weak_binders\x18\x0b \x01(\x05\x1a\x99\x02\n\x06\x46\x61\x63\x65ts\x12\x0b\n\x03tcn\x18\x01 \x01(\x05\x12\x0b\n\x03lcn\x18\x02 \x01(\x05\x12\n\n\x02\x63\x66\x18\x03 \x01(\x01\x12\x0e\n\x06purity\x18\x04 \x01(\x01\x12\x1b\n\x13\x65xpected_alt_copies\x18\x05 \x01(\x05\x12\x1b\n\x13\x63\x63\x66_expected_copies\x18\x06 \x01(\x01\x12!\n\x19\x63\x63\x66_expected_copies_lower\x18\x07 \x01(\x01\x12!\n\x19\x63\x63\x66_expected_copies_upper\x18\x08 \x01(\x01\x12\"\n\x1a\x63\x63\x66_expected_copies_prob95\x18\t \x01(\x01\x12\"\n\x1a\x63\x63\x66_expected_copies_prob90\x18\n \x01(\x01\x12\x11\n\tclonality\x18\x0b \x01(\t\x1a\xf4\x03\n\x18GetBaseCountsMultiSample\x12\x17\n\x0ft_alt_count_raw\x18\x01 \x01(\x05\x12\x17\n\x0fn_alt_count_raw\x18\x02 \x01(\x05\x12\x1b\n\x13t_alt_count_raw_fwd\x18\x03 \x01(\x05\x12\x1b\n\x13n_alt_count_raw_fwd\x18\x04 \x01(\x05\x12\x1b\n\x13t_alt_count_raw_rev\x18\x05 \x01(\x05\x12\x1b\n\x13n_alt_count_raw_rev\x18\x06 \x01(\x05\x12\x17\n\x0ft_ref_count_raw\x18\x07 \x01(\x05\x12\x17\n\x0fn_ref_count_raw\x18\x08 \x01(\x05\x12\x1b\n\x13t_ref_count_raw_fwd\x18\t \x01(\x05\x12\x1b\n\x13n_ref_count_raw_fwd\x18\n \x01(\x05\x12\x1b\n\x13t_ref_count_raw_rev\x18\x0b \x01(\x05\x12\x1b\n\x13n_ref_count_raw_rev\x18\x0c \x01(\x05\x12\x13\n\x0bt_depth_raw\x18\r \x01(\x05\x12\x13\n\x0bn_depth_raw\x18\x0e \x01(\x05\x12\x17\n\x0ft_depth_raw_fwd\x18\x0f \x01(\x05\x12\x17\n\x0fn_depth_raw_fwd\x18\x10 \x01(\x05\x12\x17\n\x0ft_depth_raw_rev\x18\x11 \x01(\x05\x12\x17\n\x0fn_depth_raw_rev\x18\x12 \x01(\x05\x1a\xfe\x01\n\x12ZygosityAnnotation\x12\x16\n\x0enum_ref_copies\x18\x01 \x01(\x05\x12\x16\n\x0enum_alt_copies\x18\x02 \x01(\x05\x12!\n\x19\x65xpected_t_alt_freq_lower\x18\x03 \x01(\x01\x12!\n\x19\x65xpected_t_alt_freq_upper\x18\x04 \x01(\x01\x12 \n\x18tumor_vaf_cn_concordance\x18\x05 \x01(\x08\x12\x19\n\x11\x61llelic_imbalance\x18\x06 \x01(\t\x12\x1e\n\x16loss_of_heterozygosity\x18\x07 \x01(\x08\x12\x15\n\rzygosity_flag\x18\x08 \x01(\t\"\xae\x02\n\x0cTempoMessage\x12\x13\n\x0b\x63moSampleId\x18\x01 \x01(\t\x12\x19\n\x11normalCmoSampleId\x18\x02 \x01(\t\x12\x17\n\x0fpipelineVersion\x18\x03 \x01(\t\x12 \n\x18genomeNexusServerVersion\x18\x04 \x01(\t\x12\"\n\x1agenomeNexusDatabaseVersion\x18\x05 \x01(\t\x12\x12\n\nvepVersion\x18\x06 \x01(\t\x12\x17\n\x0fpolyphenVersion\x18\x07 \x01(\t\x12\x13\n\x0bsiftVersion\x18\x08 \x01(\t\x12\x19\n\x11oncokbDataVersion\x18\t \x01(\t\x12\x14\n\x0concotreeCode\x18\n \x01(\t\x12\x1c\n\x06\x65vents\x18\x0b \x03(\x0b\x32\x0c.tempo.EventB:Z8github.mskcc.org/cdsi/cdsi-protobuf/tempo/tempo_types_v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tempo_maf_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z8github.mskcc.org/cdsi/cdsi-protobuf/tempo/tempo_types_v1'
  _globals['_EVENT']._serialized_start=27
  _globals['_EVENT']._serialized_end=3391
  _globals['_EVENT_NEOANTIGEN']._serialized_start=1996
  _globals['_EVENT_NEOANTIGEN']._serialized_end=2347
  _globals['_EVENT_FACETS']._serialized_start=2350
  _globals['_EVENT_FACETS']._serialized_end=2631
  _globals['_EVENT_GETBASECOUNTSMULTISAMPLE']._serialized_start=2634
  _globals['_EVENT_GETBASECOUNTSMULTISAMPLE']._serialized_end=3134
  _globals['_EVENT_ZYGOSITYANNOTATION']._serialized_start=3137
  _globals['_EVENT_ZYGOSITYANNOTATION']._serialized_end=3391
  _globals['_TEMPOMESSAGE']._serialized_start=3394
  _globals['_TEMPOMESSAGE']._serialized_end=3696
# @@protoc_insertion_point(module_scope)
