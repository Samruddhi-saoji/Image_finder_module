from duckduckgo_search import DDGS
import itertools
import requests 
import os

#to add metadata to the image
from PIL import Image
from PIL.ExifTags import TAGS


class ImageFinder :
    '''license : any (All Creative Commons), Public (PublicDomain),
            Share (Free to Share and Use), ShareCommercially (Free to Share and Use Commercially),
            Modify (Free to Modify, Share, and Use), ModifyCommercially (Free to Modify, Share, and
            Use Commercially). Defaults to None.'''
    def __init__(self, license=None) -> None:
        self.license = license
    

    ###################### create datasets ################################
    
    #get images of only 1 class
        # n = number of images
        #images will be saved in the given folder
    #if folder_path doesnt exist, a new folder will be created
    def get_data(self, folder_path, topic, n) :
        images = self.search(topic, n) #metadat of all n images
        self.save_images(images, folder_path)


    ####################### find and save images ##################################
    #returns the metadata of the recquired images
        # n = number of images
    def search(self, topic, n) :
        with DDGS() as ddgs:
            results = ddgs.images(
                keywords = topic, #what image to search
                type_image = "photo",
                license_image= self.license, 
                )
            #results = contains the metadata of ALL the images found

            #we use itertools to get the metadata only the first n images in results
            metadata = list(itertools.islice(results, n))

            return metadata


    #save all the images to the folder
    # "images_data" = contains the metadata of all images
    def save_images(self, images_data, folder_path):
        for img in images_data:
            #get url from the metadata
            url = img['image']

            dest = folder_path

            #download the image
            self.download(url, dest)


    #function to download the image from a given url
    def download(self, image_url, folder_path):
        try:
            # Create the folder if it doesn't exist
            os.makedirs(folder_path, exist_ok=True)

            #the https request
            response = requests.get(image_url)
            response.raise_for_status()  #Check for errors

            # Extract the filename from the URL
            filename = os.path.basename(image_url)

            # save address (dest) = folder path + filename 
            dest = os.path.join(folder_path, filename)

            # Save the image at the destination
            with open(dest, 'wb') as f:
                f.write(response.content)

            print(f"Image downloaded and saved at: {dest}")

        except requests.exceptions.RequestException as e:
            print("Error downloading image:", e)
            


    ################## adding metadat to each image ##################
    def add_metadata(self, image_path, metadata):
        try:
            # Open the image using Pillow
            image = Image.open(image_path)

            # Get the existing EXIF data (if any)
            exif_data = image.info.get('exif', {})

            # Convert the metadata dictionary to EXIF format
            for key, value in metadata.items():
                exif_data[TAGS.get(key, key)] = value

            # Save the image with the updated EXIF data
            image.save(image_path, exif=exif_data)

            print("Metadata added successfully!")

        except Exception as e:
            print("Error adding metadata:", e)



