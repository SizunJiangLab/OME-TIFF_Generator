![Example image](README_img/example_img.png)
# OME-TIFF Generator
This script is created to combine multiple **16 bit tiff** images into a 16 bit or 8 bit pyramidal OME-TIFF. The current version is working, but some improvements and more features will be added later.
## Python and Library Version
- `Python 3.9.6`
- `numpy 1.23.1`
- `tifffile 2022.5.4`
### Install `tifffile`
Use
`pip install tifffile` or `conda install tifffile`, if you are using conda to manage your libraries.
## Basic Usage
Requires library [`tifffile`](https://github.com/cgohlke/tifffile). This script should be run as follows:

```
python generate_ome_tiff.py <PATH> <Pixel width> <Pixel height> <Bit Depth> -o<Output>
```

For each argument, 
- `<PATH>` should be the path to the directory with the tiff files you want to combine.
- `<Pixel width>` should be the pixel width resolution from your imaging instrument in **μm**.
- `<Pixel height>` should be the pixel height resolution from your imaging instrument in **μm**.
- `<Bit Depth>` 8 bit or 16 bit
- `-o<Output name>` is an optional option that tells the program to name the output file after `<Output>`. If omitted, the output will be named after the directory and the OME-TIFF will be generated in the current working directory.

## Example

For this example, my working directory is `/Users/huayingqiu/JiangLab`.

![pwd](README_img/pwd.png)

Say I have the script and the tiffs in the following directories:

`/Users/huayingqiu/JiangLab/generate_ome_tiff.py`

![tree](README_img/tree.png)

and 

`/Users/huayingqiu/JiangLab/data`

![data](README_img/data.png)

The pixel size of the instrument is 0.38μm x 0.38μm. And I want to name the output file as `example.ome.tiff` and output into `Users/huayingqiu/JiangLab/img` as a 16 bit image. To do all these, I would run the following

`python generate_ome_tiff.py data 0.38 0.38 16 -oimg/example`

Then, voila, the pyramidal OME-TIFF is created. This OME-TIFF will be directly compatible with most readers, including the open-source Qupath.

![output](README_img/output.png)



Developed and implemented by: Huaying Qiu. Aka blame him if you have problems :) 






