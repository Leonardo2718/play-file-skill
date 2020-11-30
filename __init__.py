# Copyright (C) 2020 Leonardo Banderali
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import re
from os import walk as os_walk
from os.path import dirname, join
from mycroft import MycroftSkill, intent_file_handler
from mycroft.skills.common_play_skill import CommonPlaySkill, CPSMatchLevel
from mycroft.util.parse import match_one

class PlayFile(CommonPlaySkill):
    def __init__(self):
        super(PlayFile, self).__init__(name="PlayFileSkill")

        # regex to match "file" or "the file" in a phrase
        self.filename_re = re.compile(r"(the\s)?\s*file\s*")
        # regex to match the file extension in a file name
        self.file_extension_re = re.compile(r"\.\w+$")
        # regex to match separators in file names
        self.filename_sep_re = re.compile(r"[-_]+")

        self.media_dir = join(dirname(__file__), "media")

    def CPS_match_query_phrase(self, phrase):
        self.log.debug("Invoked with phrase: {}".format(phrase))
        if self.voc_match(phrase, "play.file"):
            self.log.info('Matched "file" vocabulary')
            filename = self.filename_re.sub("", phrase, count=1) # remove "the file" prefix
            self.log.info('Searching for "{}" in {}'.format(filename, self.media_dir))
            file_list = {self.filename_sep_re.sub(" ", self.file_extension_re.sub("", f)):join(root,f) for (root, _, files) in os_walk(self.media_dir) for f in files}
            self.log.debug(str(file_list))
            match, confidence = match_one(filename, file_list)
            self.log.debug('found match "{}" with confidence {}'.format(match, confidence))
            if confidence > 0.5:
                level = CPSMatchLevel.EXACT if confidence > 0.8 else CPSMatchLevel.TITLE
                return (phrase, level, {"file-path": match})
        return None

    def CPS_start(self, phrase, data):
        self.CPS_play(join(dirname(__file__), data["file-path"]))


def create_skill():
    return PlayFile()

