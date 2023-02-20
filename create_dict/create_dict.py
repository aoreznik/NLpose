import pysam
from pysam import VariantFile
import re
import fragment

class DictCreator(object):
	################################################################
	# Initialization / resource loading                            #
	################################################################
	def __init__(self, config, source_sam_file):
		# Counters
		################
		self.lines_processed = 0
		self.num_unmapped_reads = 0
		self.num_wrong_pos_mapping_manifest = 0
		self.num_rs_total = 0
		self.num_rs_found = 0
		self.num_hgvs = 0
		# Resources
		################
		self.load_illumina_rs_dict(config['illuminaName_rsID'])
		self.load_atlas_dict(config['atlasID_rsID'])
		self.load_hgvs_atlas_dict(config['snp_hgvs_genome'])
		self.tabixfile = VariantFile(config['dbSNP'])
		# Output files
		################
		self.out_errors = open('errors/errors.txt', 'w')
		self.out_add_to_atlas_db = open('errors/add_to_atlas_DB.txt', 'w')
		self.out_dict = open('results/dict.txt', 'w')
		# Input sam file (filter first)
		################
		filtered_sam_file = 'tmp/out_filtered.sam'
		self.filter_sam(source_sam_file, filtered_sam_file)
		self.in_sam = pysam.Samfile(filtered_sam_file, 'r')

	# Load illumina names correspodace with rsIDs
	def load_illumina_rs_dict(self, illumina_rs_dict_file):
		print 'load_illumina_rs_dict'
		self.illumina_rs_dict = dict()
		for line in open(illumina_rs_dict_file):
			line_sp = line.rstrip().split()
			if line_sp[1].split(', ')[0]!='.':
				self.illumina_rs_dict[line_sp[0]] = line_sp[1].split(', ')[0]

	# Load Atlas dictionary atlasid-rsID
	def load_atlas_dict(self, atlas_dict_file):
		print 'load_atlas_dict'
		self.atlas_dict = dict()
		for line in open(atlas_dict_file):
			line_sp = line.rstrip().split(',')
			self.atlas_dict[line_sp[1]] = line_sp[0]

	# Load atlas dictionary atlasid-HGVS
	def load_hgvs_atlas_dict(self, hgvs_atlas_dict_file):
		print 'load_hgvs_atlas_dict'
		self.hgvs_atlas_dict = dict()
		for line in open(hgvs_atlas_dict_file):
			line_sp = line.rstrip().split(',')
			self.hgvs_atlas_dict[line_sp[1]] = line_sp[0]

	def filter_sam(self, source_sam_file, filtered_sam_file):
		new = open(filtered_sam_file, 'w')
		for line in open(source_sam_file):
			if len(line.split()[0]) < 100:
				new.write(line)
			else:
				self.log_error(line.split()[0], 5)
		new.close()

	################################################################
	# Supplementary                                                #
	################################################################
	def report_progress(self):
		print 'lines processed ', self.lines_processed
		print 'unmapped reads ', self.num_unmapped_reads
		print 'wrong pos mapping manifest ', self.num_wrong_pos_mapping_manifest
		print 'rs total ', self.num_rs_total, ', rs found = ', self.num_rs_found

	# Error codes:
	# 1 - rsID is not assosiated with any AtlasID
	# 2 - HGVS is not assosiated with any AtlasID
	# 3 - no mapping position can be found
	# 4 - incorrect mapping postions (different chromosomes or too far from each other)
	# 5 - incorrect name
	def log_error(self, tag, error_code):
		self.out_errors.write(self.output_format(tag, error_code))

	def change_complimentary(self, nuclseq_arr):
		complimentary_seq_arr = []
		for nucl in nuclseq_arr:
			complimentary_seq = ''
			for i in nucl.lower():
				if nucl.lower() == 'a':
					complimentary_seq += 'T'
				elif nucl.lower() == 't':
					complimentary_seq += 'A'
				elif nucl.lower() ==  'g':
					complimentary_seq += 'C'
				elif nucl.lower() == 'c':
					complimentary_seq += 'G'
				else:
					return '#'
			complimentary_seq_arr.append(complimentary_seq)
		return complimentary_seq_arr

	def get_end_pos(self, alt, ref, pos):
		if len(ref) == len(alt) == 1:
			pos_end = int(pos)
		elif len(ref) < len(alt):
			pos_end = int(pos)
		elif len(ref) > len(alt):
			pos_end = int(pos) + len(ref[1:]) - 1
		else:
			pos_end = int(pos) + len(alt[1:]) - 1
		return pos_end

	def output_format(self, *args):
		output_str = ''
		for arg in args:
			output_str += str(arg)
			output_str += '\t'
		return output_str[:-1] + '\n' # Replace last tab with newline

	def write_to_dict(self, rs, illumina_name, ref, alt, chrom, pos_start, hgvs):
		pos_end = self.get_end_pos(alt, ref, pos_start)
		# TODO if-statememt seems broken - no atlasID in first if
		if hgvs:
			self.out_dict.write(self.output_format(illumina_name, atlasID, '*', ref, alt, chrom, pos_start, rs))
		elif rs not in self.atlas_dict:
			if rs:
				self.log_error(illumina_name, 1)
				self.out_add_to_atlas_db.write(self.output_format(illumina_name, '*', ref, alt, chrom, pos_start, pos_end, rs))
		elif not hgvs and rs in self.atlas_dict:
			atlasID = self.atlas_dict[rs]
			self.out_dict.write(self.output_format(illumina_name, atlasID, '*', ref, alt, chrom, pos_start, rs))

	################################################################
	# Main processing                                              #
	################################################################
	def get_rs(self, f):
		rs = ''
		if 'rs' in f.qname:
			self.num_rs_total += 1
			for i in re.findall(r"[\w'] + ", f.qname):
				if 'rs' in i:
					rs = 'rs' + i.split('rs')[1].split('_')[0]
		elif f.qname.split('-')[0] in self.illumina_rs_dict:
			rs = self.illumina_rs_dict[f.qname.split('-')[0]]
		return rs

	def process_dbsnp(self, f, rs):
		rs_found = False
		for gtf in self.tabixfile.fetch(f.chr1.replace('chr', ''), f.start, f.end):
			if len(gtf.alleles) < 2:
				continue
			elif len(gtf.alleles[0]) < len(gtf.alleles[1]):
				changes_dbsnp = [x[1:] for x in gtf.alleles[1:]]
				changes_dbsnp_compl = self.change_complimentary(changes_dbsnp)
			elif len(gtf.alleles[0]) == len(gtf.alleles[1])  ==  1:
				changes_dbsnp = gtf.alleles[1:]
				changes_dbsnp_compl = self.change_complimentary(changes_dbsnp)
			else:
				changes_dbsnp = ['-']
				changes_dbsnp_compl = ['-']
			if (f.alt_manifest == '-' or f.ref_manifest == '-') :
				if (len(gtf.alleles[0]) == 1 and len(gtf.alleles[1]) ==  1):
					continue
			if rs == gtf.id or \
				((int(gtf.info['RSPOS']) == f.pos_snp_first_read or int(gtf.info['RSPOS']) == f.pos_snp_second_read) and \
				(f.alt_manifest in changes_dbsnp or f.ref_manifest in changes_dbsnp or f.ref_manifest in changes_dbsnp_compl or f.alt_manifest in changes_dbsnp_compl)):
				rs_found = True
				flag_type = ''
				self.num_rs_found += 1
				rs = gtf.id
				if len(gtf.alleles[0]) == len(gtf.alleles[1]) == 1:
					ref = gtf.alleles[0]
					alt = gtf.alleles[1]
					flag_type = 'snp'
				elif len(gtf.alleles[0]) < len(gtf.alleles[1]):
					ref = '-'
					alt = gtf.alleles[1][1:]
					flag_type = 'indel'
				else:
					ref = gtf.alleles[0][1:]
					alt = '-'
					flag_type = 'indel'
				pos_start = int(f.pos_manifest)
				if not f.is_snp():
					continue
				if flag_type == 'snp':
					for alt in changes_dbsnp:
						self.write_to_dict(rs, f.illumina_name, ref, alt, f.chr1.replace('chr', ''), gtf.info['RSPOS'], 0)
				else:
					self.write_to_dict(rs, f.illumina_name, ref, alt, f.chr1.replace('chr', ''), gtf.info['RSPOS'], 0)
				break
		return rs_found

	def process_hgvs(self, f):	
		self.num_hgvs += 1

		hgvs_name = ''
		if f.chr1 == 'chrMT':
			hgvs_name += 'NC_012920.1:m.'
		elif len(f.chr1) == 1:
			hgvs_name += 'NC00000'
		else:
			hgvs_name += 'NC0000'
		if f.chr1 == 'chrY':
			chr_add = '24'
		elif f.chr1 == 'chrX':
			chr_add = '23'
		else:
			chr_add = f.chr1.replace('chr', '')

		pos_start = int(f.pos_snp_first_read)
		if 'NC_012920.1' not in hgvs_name:
			hgvs_name = hgvs_name + chr_add + '.11:g.' + str(pos_start) + f.ref_manifest + ' > ' + f.alt_manifest
		else:
			hgvs_name = hgvs_name + str(pos_start) + f.ref_manifest + ' > ' + f.alt_manifest
		if hgvs_name in self.hgvs_atlas_dict:
			self.write_to_dict(hgvs_name, f.illumina_name, f.ref_manifest, f.alt_manifest, f.chr1.replace('chr', ''), gtf.info['RSPOS'], 1)
		else:
			pos_end = self.get_end_pos(f.alt_manifest, f.ref_manifest, pos_start)
			self.out_add_to_atlas_db.write(self.output_format(f.illumina_name, '*', '*', f.ref_manifest, f.alt_manifest, \
				f.chr1, pos_start, pos_end, hgvs_name))
			self.log_error(f.illumina_name, 2)

	def process_fragment(self, f):
		if f.chr1 != f.chr2 or f.chr2 == 'chr0' or f.chr1 == 'chr0' or f.chr1 != f.chrom_manifest:
			self.log_error(f.illumina_name, 4)
			self.num_wrong_pos_mapping_manifest += 1
			return

		rs = self.get_rs(f)
		rs_found = self.process_dbsnp(f, rs)
		if not rs_found:
			self.process_hgvs(f)

	def run(self):
		# Dictionary for first reads
		# key - qname, value - length
		# add record when first read observed, remove when second read observed
		first_read_lengths_dict = dict()
		for pysam_read in self.in_sam.fetch():
			# Report stats every 50.000 lines
			self.lines_processed += 1
			if self.lines_processed % 50000 == 0:
				self.report_progress()
			# Discard unmapped reads
			if pysam_read.tid  < 0 :
				print pysam_read.qname
				self.num_unmapped_reads += 1
				self.log_error(illumina_name, 3)
				continue
			# Store first read of fragment, process second
			if pysam_read.qname not in first_read_lengths_dict:
				first_read_lengths_dict[pysam_read.qname] = pysam_read.query_alignment_length
				continue
			else:
				first_read_length = first_read_lengths_dict[pysam_read.qname]# Get first read length
				first_read_lengths_dict.pop(pysam_read.qname)# Remove first record length
				f = fragment.Fragment(self.in_sam, pysam_read, first_read_length)
				self.process_fragment(f)
		# Finally report stats again after processing finished
		self.report_progress()

################################################################
# TODO: move somewhere else
################################################################
#monogen_rs = set()
#monogen_hgvs = set()
#for line in open('monogen.txt'):
#	if 'rs' in line:
# 		monogen_rs.add(line.rstrip())
# 	else:
# 		monogen_hgvs.add(line.rstrip())
#illumina_id_set = set()
#for line in open('illuminaname_rsid_hgvs.txt'):
#	line_sp = line.split()
#	if line_sp[0] in monogen_hgvs:
#		illumina_id_set.add(line_sp[1])
