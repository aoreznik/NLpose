import os 
import yaml
import optparse

import make_fasta
import create_dict

# Parse command line arguments to get config file name
parser = optparse.OptionParser()
parser.add_option('-c', '--config', dest = 'config_file_name', help = 'Name of configuration file to use')
(options, args) = parser.parse_args()

# Load configuration
config_file = open(options.config_file_name)
config = yaml.load(config_file)
config_file.close()

# Create missing directories
print 'Creating missing directories...'
if not os.path.isdir('tmp/'):
	os.makedirs('tmp/')
if not os.path.isdir('errors/'):
	os.makedirs('errors/')
if not os.path.isdir('results/'):
	os.makedirs('results/')

print '================================'

# Create fasta files if not yet
rs1_file = 'tmp/reads_rs1.fasta'
rs2_file = 'tmp/reads_rs2.fasta'
if not os.path.exists(rs1_file) or not os.path.exists(rs2_file):
	print 'Creating fasta files...'
	make_fasta.make_fasta(config, rs1_file, rs2_file)
else:
	print 'Fasta files exist, skip'

print '================================'

# Run aligner
sam_file = 'tmp/out.sam'
aligner_cmd = '/home/bio/bwa-0.7.15/bwa mem' + \
			' -t '+ config['numb_threads'] + ' ' + \
			config['ref_genome'] + ' ' + rs1_file + ' ' + rs2_file + ' > ' + sam_file
if not os.path.exists(sam_file):
	print 'Running aligner...'
	print aligner_cmd
	os.system(aligner_cmd)
else:
	print 'Sam file exists, skip'

print '================================'

# Create dictionary
dict_creator = create_dict.DictCreator(config, sam_file)
dict_creator.run()
