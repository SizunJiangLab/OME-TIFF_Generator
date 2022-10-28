import os 
import sys
import numpy as np
import tifffile

#####################################
# Parse command line arguments
#####################################

# Need to improve how the script parse options. Probably write a dedicated function for this
# and save seperately so we can recycle it and use it in future scripts

# Parse options. If opts is empty, it is equivalent to FALSE.  

opts = [opt for opt in sys.argv[1:] if opt.startswith('-')]

if opts:
    ALTERNATIVE_OUTPUT = True
else:
    ALTERNATIVE_OUTPUT = False

try: 
    PATH = sys.argv[1]
    RESOLUTION_X = sys.argv[2]
    RESOLUTION_Y = sys.argv[3]
    BIT_DEPTH = sys.argv[4]
except IndexError:
    raise SystemExit(f"Please input the following arguments.\
        \n Usage: {sys.argv[0]} <Path> <Resolution_X> <Resolution_Y> -o<Output name>\
        \n <PATH> : Path to the directory with TIFF files you want to combine. \
        \n <Resolution_X> : Pixel width in μm. \
        \n <Resolution_Y> : Pixel height in μm. \
        \n <BIT_DEPTH>: 8 bit or 16 bit. \
        \n -o : Specifies an alternative output name. If omitted, the output will be named after the directory.")
    

#####################################
# User inputs
#####################################

# pixel width in μm
RESOLUTION_X = sys.argv[2]
# pixel height in μm
RESOLUTION_Y = sys.argv[3]

# bit depth
BIT_DEPTH = sys.argv[4]

# Set img directory

img_dir = sys.argv[1]

# Get tiff names in img_dir

extensions = ['tif', 'tiff']

img_names = [file for file in os.listdir(img_dir) if any(file.endswith(ext) for ext in extensions)]

# remove .tiff for channel names 

channel_names = [elem.split('.')[0] for elem in img_names]

###############################################
#  Load tiff files into array and stack them
###############################################

#images = [img_dir + '/' + img for img in img_names]

imgList = list() # Create an empty list to store image arrays

# Read tiff and append to the list
for img in img_names:
    img_path = img_dir + '/' + img
    tiff = tifffile.imread(img_path)
    imgList.append(tiff)

# Stack arrays
imgStack = np.stack(imgList)

if BIT_DEPTH == '16':
    imgStack = imgStack.astype('uint16')
elif BIT_DEPTH == '8':
    imgStack[:,...] = (imgStack[:,...]/256)
    imgStack = imgStack.astype('uint8')

#########################################################
# Write pyramidal OME-TIFF
#########################################################

if ALTERNATIVE_OUTPUT:
    output_name = opts[0].split('-o')[1]
else: 
    output_name = os.path.split(img_dir)[-1]

tif_name = output_name + '.ome.tif'

with tifffile.TiffWriter(tif_name, bigtiff=True) as tif:
    options = dict(tile = (128, 128),
                    metadata = {'Channel': {'Name': channel_names},
                    'Pixels' : {
                        'PhysicalSizeX': RESOLUTION_X,
                        'PysicalSizeXUnit': 'µm',
                        'PhysicalSizeY': RESOLUTION_Y,
                        'PysicalSizeYUnit': 'µm'
                    }
                    })
    tif.write(imgStack, subifds = 4, **options)
    tif.write(imgStack[:, ::2, ::2], subfiletype = 1, **options)
    tif.write(imgStack[:, ::4, ::4], subfiletype = 1, **options)
    tif.write(imgStack[:, ::8, ::8], subfiletype = 1, **options)
    tif.write(imgStack[:, ::16, ::16], subfiletype = 1, **options)
