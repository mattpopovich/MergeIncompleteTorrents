# Merge Incomplete Torrents
# Author: Matt Popovich (popovich.matt@gmail.com)
# Date: 5/2/2020

# Note:

# Improvements:

# Imports
import logging  # debug, info, warning, error, critical
import os       # For getting the size of a file
import sys      # For exiting main()
from tqdm import tqdm   # Progress bar

logging.basicConfig()
logger = logging.getLogger('__mergeIncompleteTorrents__')
logger.setLevel(logging.DEBUG)  # What levels should be printed out to the console

# Global variables

# Functions


def checkNextBytes(fileHandlers, bytesToRead, iterNum):
    outBytes = b'\x00'
    debugString = ''
    for f in fileHandlers:
        inBytes = f.read(bytesToRead)
        if int.from_bytes(inBytes, 'big') != 0:
            if int.from_bytes(outBytes, 'big') == 0:
                outBytes = inBytes
                debugString += '1'
            else:   # inBytes and outBytes both have values
                if outBytes != inBytes:
                    # These pieces are different from each other, these files are not the same
                    # logger.error("Piece {} starting at byte {} differ between the files".format(iterNum, iterNum * bytesToRead))
                    logger.error("Difference in the files: {} != {}".format(outBytes, inBytes))
                    debugString += 'x'
                    sys.exit(2)  # Exit with failure
                else:
                    debugString += '1'
        else:
            debugString += '0'

    return (outBytes, debugString)


def main():

    outputFileName = '/Users/mattpopovich/Downloads/outputFileTest'
    # of = open(outputFileName, 'wb')

    inputFileNames = []
    # inputFileNames.append("test")

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

    # Create file handlers
    fileHandlers = []
    for f in inputFileNames:
        fileHandlers.append(open(f, 'rb'))

    # Read files
    iterationSizeBytes = pow(2,20)  # Minimum piece size of 16kB
    completeFile = True

    numLoops = int(inputFileSizes[0]/iterationSizeBytes)    # This will round down
    logger.info("numLoops: {}".format(numLoops))

    blanks = 0
    data = 0
    collisions = 0

    for b in tqdm(range(numLoops)):
        outBytes, debugString = checkNextBytes(fileHandlers, iterationSizeBytes, b)

        if 'x' in debugString:
            logger.error("Piece {} starting at byte {} differ between the files: {}".format(b, b * iterationSizeBytes, debugString))
            collisions += 1

        if int.from_bytes(outBytes, 'big') == 0:
            logger.warning("Iteration {} starting at byte {} will be blank".format(b, b*iterationSizeBytes))
            completeFile = False
            blanks += 1
        else:
            logger.debug("Iteration {} starting at byte {} will not be blank: {}".format(b, b*iterationSizeBytes, debugString))
            data += 1

        # TODO: Write to output file

    # Read the very last piece of the file
    remainingToRead = inputFileSizes[0] % iterationSizeBytes
    if remainingToRead != 0:
        logger.info("Reading very last piece of file, {} bytes".format(remainingToRead))
        outBytes, debugString = checkNextBytes(fileHandlers, remainingToRead, 1)

        if 'x' in debugString:
            logger.error("Piece {} starting at byte {} differ between the files: {}".format(1, remainingToRead, debugString))
            collisions += 1

        if int.from_bytes(outBytes, 'big') == 0:
            logger.warning("Iteration {} starting at byte {} will be blank".format(1, remainingToRead))
            completeFile = False
            blanks += 1
        else:
            logger.debug("Iteration {} starting at byte {} will not be blank: {}".format(1, remainingToRead, debugString))
            data += 1

        # TODO: Write to output file



    if not completeFile:
        logger.warning("This file will not be 100% complete once finished assembling")


    logger.info("Statistics:")
    logger.info("Blanks = {} ({}), data = {} ({}), collisions = {} ({})".format(
        blanks, blanks/numLoops, data, data/numLoops, collisions, collisions/numLoops)) # This will be one short if we do an extra loop at the end (remainingToRead>0)


if __name__ == "__main__":
    main()
