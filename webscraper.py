class Scraper:
    """
    This class is used to create an image web scraper
    """

    def __init__(self, header, directory):
        #  initialization
        self.header = header
        self.directory = directory

    def __str__(self):
        return """
    Methods Available:
    .scrape(): extracts tags of interest
    .download_images(): downloads images using src extracted from tags
    .duplicate_check(): checks directory for duplicate images
    .find_duplicates(): checks is duplicates of particular instances exits and deletes them
    .delete_all(): deletes all instances of a list of images

    """

    def __repr__(self):
        return f"""
    working directory: {self.directory}
    header: {self.header}
    """

    def scrape(self, url, tag, attribute_dict, pages=1):
        """
        This method extracts img tags. Inspect to extract src.
        """
        #  importing libraries
        from urllib.request import urlopen
        import urllib.request
        from bs4 import BeautifulSoup
        import numpy as np
        import os
        import requests
        import cv2
        from tqdm import tqdm

        images = []
        for i in tqdm(range(pages)):
            request = urllib.request.Request(os.path.join(url, f'?page={str(i)}'),
                                             headers=self.header)
            html = urlopen(request)
            bs = BeautifulSoup(html.read(), 'html.parser')
            image_tags = bs.find_all(tag, attrs=attribute_dict)

            for image_tag in image_tags:
                images.append(image_tag)

        return images

    def download_images(self, src_list, prefix='img'):
        """
        This method downloads scraped images into a specified directory
        """
        #  importing libraries
        from urllib.request import urlopen
        import urllib.request
        from bs4 import BeautifulSoup
        import numpy as np
        import os
        import requests
        import cv2
        from tqdm import tqdm

        try:
            os.mkdir(self.directory)
        except FileExistsError:
            def sort_key(element):
                return int(element.split('.')[0].split('_')[1])

            file_names = os.listdir(self.directory)
            file_names.sort(reverse=False, key=sort_key)
            image_count = int(file_names[-1].split('.')[0].split('_')[1]) + 1

            for src in tqdm(src_list):
                with open(os.path.join(self.directory, prefix + f'_{str(image_count)}.jpg'),
                          'wb') as f:
                    response = requests.get(src)
                    f.write(response.content)
                image_count += 1

        print('Done!')

    def duplicate_check(self):
        #  importing libraries
        from urllib.request import urlopen
        import urllib.request
        from bs4 import BeautifulSoup
        import numpy as np
        import os
        import requests
        import cv2
        from tqdm import tqdm

        #  creating empty lists to hold images
        images = []
        temp_list = []

        #  defining a function which helps to check if an element is part of a list
        def gate(file_list, master_list):
            if len(master_list) == 0:
                return 'allow'
            #  function logic
            access = []
            for li in master_list:
                check = np.array_equal(file_list[0], li[0])
                access.append(check)
                if check == True:
                    break
            #  return statement
            if True in access:
                return 'deny'
            else:
                return 'allow'

        #  reading images into list
        print('reading images...')
        for f in tqdm(os.listdir(self.directory)):
            try:
                image = cv2.imread(os.path.join(self.directory, f), cv2.IMREAD_GRAYSCALE)
                image = cv2.resize(image, (20, 20))
                images.append([image, f])
            except Exception:
                pass

        #  replicating list of images
        images_2 = [x for x in images]

        #  checking images for duplicate instances
        print('\nchecking images...')
        for image in tqdm(images):
            i = 0
            images_2.remove(image)
            for img in images_2:
                if np.array_equal(image[0], img[0]):
                    i += 1
                    if i == 1:
                        temp_list.append(image)
                        break

        #  creating list to hold refined duplicates
        duplicates_3 = []

        #  refining list of duplicates
        print('processing...')
        for image_file in tqdm(temp_list):
            if gate(image_file, duplicates_3) == 'allow':
                duplicates_3.append(image_file)

        #  deriving filenames form refined list
        duplicates = [x[1] for x in duplicates_3]

        #  printing to screen
        if len(duplicates) > 1:
            print(f'\nThere are {len(duplicates)} duplicated instances in the dataset')
        elif len(duplicates) == 0:
            print(f'\nThere are no duplicated instances in the dataset')
        else:
            print(f'\nThere is {len(duplicates)} duplicated instance in the dataset')
        return duplicates

    def find_duplicates(self, filenames=[]):
        """
        This method checks if particular images are duplicated providing the option
        of deleting them or not.
        """
        #  importing libraries
        from urllib.request import urlopen
        import urllib.request
        from bs4 import BeautifulSoup
        import numpy as np
        import os
        import requests
        import cv2
        from tqdm import tqdm

        to_check = []
        #  creating a list to hold duplicates
        all_duplicates = []

        #  Appending duplicated images array to list
        for f in tqdm(filenames):
            instance = cv2.imread(os.path.join(self.directory, f))
            to_check.append(instance)

        #  looping through all files
        for f in tqdm(os.listdir(self.directory)):
            #  reading image files
            image_instance = cv2.imread(os.path.join(self.directory, f))
            #  looping through all images to be checked
            for item in to_check:
                #  comparing arrays
                check = np.array_equal(image_instance, item)
                if check:
                    #  appending duplicate to list if condition holds true
                    all_duplicates.append(f)

        if len(to_check) == len(all_duplicates):
            print('\nThere are no duplicated instances.')
        else:
            print(f'\nTotal number of duplicates:' +
                  f' {len(all_duplicates[len(to_check):])}')

        request_input = True

        while request_input:
            user_input = input('Would you like to delete duplicates? (Yes(y)/No(n)): ')

            if user_input.lower() == 'y':
                all_duplicates = [x for x in all_duplicates if x not in filenames]
                for instance in tqdm(all_duplicates):
                    try:
                        os.remove(os.path.join(self.directory, instance))
                    except FileNotFoundError:
                        pass
                print('\nDone!')
                request_input = False
            elif user_input.lower() == 'n':
                print('Done!')
                request_input = False
            else:
                print('Invalid Input!')

    def delete_all(self, filenames):
        """
        This method deletes all instances of a particular image.
        """
        #  importing libraries
        from urllib.request import urlopen
        import urllib.request
        from bs4 import BeautifulSoup
        import numpy as np
        import os
        import requests
        import cv2
        from tqdm import tqdm

        to_check = []
        #  creating a list to hold duplicates
        all_duplicates = []

        #  Appending image instance array to list
        for f in tqdm(filenames):
            instance = cv2.imread(os.path.join(self.directory, f))
            to_check.append(instance)

        #  looping through all files
        for f in tqdm(os.listdir(self.directory)):
            #  reading image files
            image_instance = cv2.imread(os.path.join(self.directory, f))
            #  looping through all images to be checked
            for item in to_check:
                #  comparing arrays
                check = np.array_equal(image_instance, item)
                if check:
                    #  appending duplicate to list if condition holds true
                    all_duplicates.append(f)

        while True:
            user_input = input(f'There are/is {len(all_duplicates)} instances in this dataset.' +
                               "\nConfirm deletion (Confirm(c)/Cancel(x)): ")

            if user_input.lower() == 'c':
                #  deleting images
                try:
                    for instance in all_duplicates:
                        os.remove(os.path.join(self.directory, instance))
                except FileNotFoundError:
                    pass
                break
            elif user_input.lower() == 'x':
                pass
                break
            else:
                print('Invalid Input!\n')
        print('\nDone!')
        