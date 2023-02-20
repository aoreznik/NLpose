class Fragment(object):

	def __init__(self, sam_in, read, first_read_length):
		self.indel_len = int(read.qname.split('_')[-3])
		self.qname = read.qname
		self.chrom_manifest = 'chr' + read.qname.split('_')[-1]
		self.pos_manifest = int(read.qname.split('_')[-2])
		self.alt_manifest = read.qname.split('_')[-4].split('/')[1]
		self.ref_manifest = read.qname.split('_')[-4].split('/')[0]
		self.illumina_name = read.qname.split('/')[0].replace('_' + read.qname.split('/')[0].split('_')[-1], '')
		
		self.chr1 = sam_in.getrname(read.tid)
		self.chr2 = sam_in.getrname(read.rnext)
		self.normalize_chrom_names()

		if not read.is_reverse:
			self.pos_snp_second_read = read.pos
		else:
			self.pos_snp_second_read = read.pos + read.query_alignment_length + 1

		if read.mate_is_reverse:
			self.pos_snp_first_read = read.next_reference_start
		else:
			self.pos_snp_first_read = read.next_reference_start + first_read_length + 1

		self.start = min(self.pos_snp_first_read, self.pos_snp_second_read) - 20
		self.end = min(self.start + 1000, max(self.pos_snp_first_read, self.pos_snp_second_read) + 20)

	def normalize_chrom_names(self):
		if self.chr1 == 'chr24':
			self.chr1 = 'chrY'
			self.chr2 = 'chrY'
		elif self.chr1 == 'chr23':
			self.chr1 = 'chrX'
			self.chr2 = 'chrX'
		elif self.chr1 == 'chrM':
			self.chr2 = 'chrMT'
			self.chr1 = 'chrMT'

	def is_snp(self):
		return len(self.alt_manifest) == len(self.ref_manifest) == 1 # Otherwise indel