#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#  Copyright 2015 Erik Daguerre <fallenwolf@meddlesomewolf.com>
#  Special thanks to @zeroSteiner for help debugging and suggestions
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following disclaimer
#    in the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of the  nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#

import re
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '3.0')

from gi.repository import Gtk
from gi.repository import GtkSource
from gi.repository import GObject


class CustomCompletionProvider(GObject.GObject, GtkSource.CompletionProvider):
	"""
	This is a custom Completion Provider
	In this instance, it will do 2 things;

	1) always provide Hello World! (Not ideal but an option so its in the example)

	2) Utilizes the Gtk.TextIter from the TextBuffer to determine if there is a jinja
	example of '{{ custom.' if so it will provide you with the options of foo and bar.
	if select it will insert foo }} or bar }}, completing your syntax

	PLEASE NOTE the GtkTextIter Logic and regex are really rough and should be adjusted and tuned
	to fit your requirements

	# Implement the Completion Provider
	# http://stackoverflow.com/questions/32611820/implementing-gobject-interfaces-in-python
	# https://gist.github.com/andialbrecht/4463278 (Python example implementing TreeModel)
	# https://developer.gnome.org/gtk3/stable/GtkTreeModel.html (Gtk TreeModel interface specification)
	# A special thank you to @zeroSteiner
	"""

	# apparently interface methods MUST be prefixed with do_
	def do_get_name(self):
		return 'Custom'

	def do_match(self, context):
		# this should evaluate the context to determine if this completion
		# provider is applicable, for debugging always return True
		return True

	def do_populate(self, context):
		proposals = [
			GtkSource.CompletionItem(label='Hello World!', text='Hello World!', icon=None, info=None)  # always proposed
		]

		# found difference in Gtk Versions
		end_iter = context.get_iter()
		if not isinstance(end_iter, Gtk.TextIter):
			_, end_iter = context.get_iter()

		if end_iter:
			buf = end_iter.get_buffer()
			mov_iter = end_iter.copy()
			if mov_iter.backward_search('{{', Gtk.TextSearchFlags.VISIBLE_ONLY):
				mov_iter, _ = mov_iter.backward_search('{{', Gtk.TextSearchFlags.VISIBLE_ONLY)
				left_text = buf.get_text(mov_iter, end_iter, True)
			else:
				left_text = ''

			if re.match(r'.*\{\{\s*custom\.$', left_text):
				proposals.append(
					GtkSource.CompletionItem(label='foo', text='foo }}')  # optionally proposed based on left search via regex
				)
				proposals.append(
					GtkSource.CompletionItem(label='bar', text='bar }}')  # optionally proposed based on left search via regex
				)

		context.add_proposals(self, proposals, True)
		return

class SimpleProgram(object):

	def __init__(self):
		self.builder = Gtk.Builder()
		GObject.type_register(GtkSource.View)
		self.builder.add_from_file("main.glade")
		self.main_window = self.builder.get_object("MainWindow")
		self.view = self.builder.get_object("View")
		self.textbuff = GtkSource.Buffer()
		self.view.set_buffer(self.textbuff)
		self.lm = GtkSource.LanguageManager()
		self.textbuff.set_language(self.lm.get_language('python'))
		self.main_window.connect("destroy", Gtk.main_quit)

		self.keywords = """
				GtkSourceView
				Completion
			"""

	def show(self):
		self.set_auto_completation()
		self.main_window.show_all()

	def set_auto_completation(self):
		"""
		1)
		Set up a provider that get words from what has already been entered
		in the gtkSource.Buffer that is tied to the GtkSourceView

		2)
		Set up a second buffer that stores the keywords we want to be available

		3)
		Setup an instance of our custome completion class to handle special characters with
		auto complete.
		"""
		# This gets the GtkSourceView completion that's already tied to the GtkSourceView
		# We need it to attached our providers to it
		self.view_completion = self.view.get_completion()

		# 1) Make a new provider, attach it to the main buffer add to view_autocomplete
		self.view_autocomplete = GtkSource.CompletionWords.new('main')
		self.view_autocomplete.register(self.textbuff)
		self.view_completion.add_provider(self.view_autocomplete)

		# 2) Make a new buffer, add a str to it, make a provider, add it to the view_autocomplete
		self.keybuff = GtkSource.Buffer()
		self.keybuff.begin_not_undoable_action()
		self.keybuff.set_text(self.keywords)
		self.keybuff.end_not_undoable_action()
		self.view_keyword_complete = GtkSource.CompletionWords.new('keyword')
		self.view_keyword_complete.register(self.keybuff)
		self.view_completion.add_provider(self.view_keyword_complete)

		# 3) Set up our custom provider for syntax completion.
		custom_completion_provider = CustomCompletionProvider()
		self.view_completion.add_provider(custom_completion_provider)
		self.custom_completion_provider = custom_completion_provider
		return


def main():
	gui = SimpleProgram()
	gui.show()
	Gtk.main()

if __name__ == '__main__':
	main()

