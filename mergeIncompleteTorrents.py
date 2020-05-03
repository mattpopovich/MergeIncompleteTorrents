# Merge Incomplete Torrents
# Author: Matt Popovich (popovich.matt@gmail.com)
# Date: 5/2/2020

# Note:

# Improvements:

# Imports
import logging  # debug, info, warning, error, critical
import os       # For getting the size of a file
import sys      # For exiting main()

logging.basicConfig()
logger = logging.getLogger('__mergeIncompleteTorrents__')
logger.setLevel(logging.DEBUG)  # What levels should be printed out to the console

# Global variables

# Functions


def main():

    outputFileName = '/Users/mattpopovich/Downloads/outputFileTest'
    # of = open(outputFileName, 'wb')

    inputFileNames = []
    inputFileNames.append("test")

    # Check to make sure input files have the same file size
    inputFileSizes = []
    for f in inputFileNames:
        fileSize = os.path.getsize(f)
        logger.debug("Filesize of {} is {} bytes".format(f, fileSize))
        inputFileSizes.append(fileSize)

    for i in range(len(inputFileSizes)-1):
        if inputFileSizes[i] != inputFileSizes[i+1]:
            logger.error("File {} = {} bytes has a different size than file {} = {} bytes".format(
                inputFileNames[i], inputFileSizes[i], inputFileNames[i+1], inputFileSizes[i+1]))
            sys.exit(1)     # Exit with failure
    logger.info("Success: all files have the same filesize")







    # bytes1 = file1.read(1024)
    # bytes2 = file2.read(1024)
    # if not bytes1 or not bytes2:
    #     break
    # bytes3 = [b1 | b2 for (b1, b2) in zip(bytes1, bytes2)]
    # file3.write(bytes3)



if __name__ == "__main__":
    main()
