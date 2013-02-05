import os

class BriskObserver:

    def update(self, brisk):
        with open('www/temp.html', 'w') as out:
            out.write(brisk.get_map_svg())
        os.rename('www/temp.html', 'www/map.svg.html')