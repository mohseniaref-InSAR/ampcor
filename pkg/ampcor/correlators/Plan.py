# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# parasim
# (c) 1998-2019 all rights reserved
#


# framework
import ampcor


# declaration
class Plan:
    """
    Encapsulation of the computational work necessary to refine an offset map between a
    {reference} and a {target} image
    """


    # public data
    # known at construction
    tile = None      # my shape as a grid of correlation pairs
    chip = None      # the shape of the reference chip
    padding = None   # the padding to apply to form the search window in the target raster
    # deduced
    window = None    # the window in the target raster
    reference = None # the sequence of reference tiles
    target = None    # the sequence of target search windows


    @property
    def pairs(self):
        """
        Yield valid pairs of reference and target tiles
        """
        # go through my tile containers
        for ref, tgt in zip(self.reference, self.target):
            # invariant: either both are good, or both are bad
            if ref and tgt:
                # yield them
                yield ref, tgt
        # all done
        return


    @property
    def footprint(self):
        """
        Compute the total amount of memory required to store the reference and target tiles
        """
        # the reference footprint
        ref = sum(tile.footprint for tile in filter(None, self.reference))
        # the target footprint
        tgt = sum(tile.footprint for tile in filter(None, self.target))
        # all done
        return ref, tgt


    # interface
    def show(self, channel):
        """
        Display details about this plan in {channel}
        """
        # sign on
        channel.line(f" -- plan:")
        # tile info
        channel.line(f"        shape: {self.tile.shape}, layout: {self.tile.layout}")
        channel.line(f"        pairs: {len(self)} out of {self.tile.size}")
        # memory footprint
        refFootprint, tgtFootprint = self.footprint
        channel.line(f"        footprint:")
        channel.line(f"            reference: {refFootprint} bytes")
        channel.line(f"               target: {tgtFootprint} bytes")

        # go through the pairs
        for offset, (ref,tgt) in enumerate(zip(self.reference, self.target)):
            # compute the index of this pair
            index = self.tile.index(offset)
            # if this is a valid pair
            if ref and tgt:
                # identify the pair
                channel.line(f"        pair: {index}")
                # show me the reference slice
                channel.line(f"            ref:")
                ref.show(channel)
                # and the target slice
                channel.line(f"            tgt:")
                tgt.show(channel)
            # otherwise
            else:
                # identify the pair as invalid
                channel.line(f"        pair: {index} INVALID")

        # all done
        return


    # meta-methods
    def __init__(self, correlator, regmap, rasters, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my tile
        self.tile = regmap.tile

        # get the reference tile size
        self.chip = correlator.chip
        # and the search window padding
        self.padding = correlator.padding
        # compute the target window shape
        self.window = tuple(c+2*p for c,p in zip(self.chip, self.padding))

        # initialize my containers
        self.reference, self.target = self.assemble(regmap=regmap, rasters=rasters)

        # all done
        return


    def __len__(self):
        """
        By definition, my length is the number of valid tile pairs
        """
        # invariant: either both tiles are good, or both are bad
        return len(tuple(filter(None, self.reference)))


    def __getitem__(self, index):
        """
        Behave like a grid
        """
        # ask my shape tile to resolve the index
        offset = self.tile.offset(index)
        # grab the corresponding tiles
        ref = self.reference[offset]
        tgt = self.target[offset]
        # and return them
        return ref, tgt


    # implementation details
    def assemble(self, rasters, regmap):
        """
        Form the set of pairs of tiles to correlate in order to refine {regmap}, a coarse offset
        map from a reference image to a target image
        """
        # unpack the rasters
        reference, target = rasters
        # get the reference tile size
        chip = self.chip
        # and the search window padding
        padding = self.padding

        # initialize the tile containers
        referenceTiles = []
        targetTiles = []

        # go through matching pairs of points in the initial guess
        for ref, tgt in zip(regmap.domain, regmap.codomain):
            # form the upper left hand corner of the reference tile
            begin = tuple(r - c//2 for r,c in zip(ref, chip))
            # attempt to make a slice; invalid specs get rejected by the slice factory
            refSlice = reference.slice(begin=begin, shape=chip)

            # the upper left hand corner of the target tile
            begin = tuple(t - c//2 - p for t,c,p in zip(tgt, chip, padding))
            # and its shape
            shape = tuple(c + 2*p for c,p in zip(chip, padding))
            # try to turn this into a slice
            tgtSlice = target.slice(begin=begin, shape=shape)

            # if both slices are valid
            if refSlice and tgtSlice:
                # push them into their respective containers
                referenceTiles.append(refSlice)
                targetTiles.append(tgtSlice)
            # otherwise
            else:
                # push invalid slices for both of them
                referenceTiles.append(None)
                targetTiles.append(None)

        # all done
        return referenceTiles, targetTiles


# end of file
