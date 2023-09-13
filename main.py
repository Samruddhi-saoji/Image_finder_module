from image_finder import ImageFinder


finder = ImageFinder("any")
finder.get_data("folder_name", "topic", 10)


'''
syntax:

finder = ImageFinder(license)
    # types of license:
        any (All Creative Commons), 
        Public (PublicDomain),
        Share (Free to Share and Use), 
        ShareCommercially (Free to Share and Use Commercially),
        Modify (Free to Modify, Share, and Use), 
        ModifyCommercially (Free to Modify, Share, and Use Commercially). 
    # Defaults = None.

finder.get_data("folder path", "topic", number of images)
'''