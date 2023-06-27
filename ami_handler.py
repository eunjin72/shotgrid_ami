import sys
import os
import re
import six
import logging as logger

import shotgun_api3

logfile_path = os.path.join(os.path.dirname(sys.argv[0]), "./log/")
if not os.path.exists(logfile_path):
    os.mkdir(logfile_path)
LOGFILE = os.path.dirname(logfile_path) + "/ami_handler.log"

# Shotgrid Api connect
SERVER_PATH = "shotgrid_url"
SCRIPT_NAME = 'script_name'
SCRIPT_KEY = 'script_key'
sg = shotgun_api3.Shotgun(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY)


class ShotgunActionException(Exception):
    pass


class ShotgunAction:
    def __init__(self, url):
        self.logger = self._init_log(LOGFILE)

        self.url = url
        self.protocol, self.action, self.params = self._parse_url()

        # ids of entities that were currently selected
        self.selected_ids = []
        if len(self.params["selected_ids"]) > 1:
            sids = self.params["selected_ids"].split(",")
            self.selected_ids = [int(id) for id in sids]

        else:
            self.selected_ids = self.params["selected_ids"]

        self.entity_type = self.params["entity_type"]

    def check_action(self):
        if self.action == 'download_mp4':
            self.download()

        else:
            print("No Action")

    def download(self, dir_path):
        for selected_id in self.selected_ids:
            version = sg.find_one(self.entity_type, [['id', 'is', int(selected_id)]], ['sg_uploaded_movie'])
            local_file_path = dir_path + "/" + re.sub(r"\s+", '_', version['sg_uploaded_movie']['name'])
            sg.download_attachment(version['sg_uploaded_movie'], file_path=local_file_path)
        print("Save")

    def _init_log(self, filename="ami_handler.log"):
        try:
            logger.basicConfig(
                level=logger.DEBUG,
                format="%(asctime)s %(levelname)-8s %(message)s",
                datefmt="%Y-%b-%d %H:%M:%S",
                filename=filename,
                filemode="w+",
            )
        except IOError as e:
            raise ShotgunActionException("Unable to open LOGFILE for writing: %s" % e)
        logger.info("ami_handler logging started.")
        return logger

    def _parse_url(self):
        logger.info("Parsing full url received: %s" % self.url)

        # get the protocol used
        protocol, path = self.url.split(":", 1)
        logger.info("protocol: %s" % protocol)

        # extract the action
        action, params = path.split("?", 1)
        action = action.strip("/")
        logger.info("action: %s" % action)

        # extract the parameters
        params = params.split("&")
        p = {"column_display_names": [], "cols": []}
        for arg in params:
            key, value = map(six.moves.urllib.parse.unquote, arg.split("=", 1))
            if key == "column_display_names" or key == "cols":
                p[key].append(value)
            else:
                p[key] = value
        params = p
        logger.info("params: %s" % params)
        return protocol, action, params


def main():
    try:
        sa = ShotgunAction(sys.argv[1])
        logger.info("ami_handler: Firing... %s" % (sys.argv[1]))

    except IndexError as e:
        raise ShotgunActionException("Missing GET arguments")
    logger.info("ami_handler process finished.")

    sa.check_action()
    sa.download(dir_path=input("Enter the directory to save : "))


if __name__ == "__main__":
    main()
