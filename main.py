#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  bmp_header.py
#
#  Copyright 2015 Erik Daguerre <fallenwolf@meddlesomewolf.com>
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
from gi.repository import Gtk
from gi.repository import GtkSource
from gi.repository import GObject

class Simple_Program(object):

	def __init__(self):
		self.builder = Gtk.Builder()
		GObject.type_register(GtkSource.View)
		self.builder.add_from_file("main.glade")
		self.main_window = self.builder.get_object("MainWindow")
		self.view = self.builder.get_object("View")
		self.textbuff = GtkSource.Buffer()
		self.view.set_buffer(self.textbuff)
		self.lm = GtkSource.LanguageManager()
		self.textbuff.set_language(self.lm.get_language('html'))
		self.main_window.connect("destroy", Gtk.main_quit)

		self.codelist = """
			{{jinja}}
			{{jinja.foo}}
			{{jinja.bar}}
			<!DOCTYPE html>
			<html> </html>
			<a href="{{ foo }}">{{ bar }}</a>
			<img src="{{ dat_pic }}"/>
			<table> </table>
			<td> </td>
			<tr> </tr>
			<style format="text/css"> </style>
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
		Set up a second buffer that stores the coding tags we want to add
		As this thing uses buffers for words don't ask me why
		"""
		# This gets the GtkSourceView completation thats already tied to the GtkSourceView
		# We need it to attached our providers to it
		self.view_completion = self.view.get_completion()

		# 1) Make a new provider, attach it to the main buffer add to view_autocomplete
		self.view_autocomplete = GtkSource.CompletionWords.new('main')
		self.view_autocomplete.register(self.textbuff)
		self.view_completion.add_provider(self.view_autocomplete)

		# 2) Make a new buffer, add a str to it, make a provider, add it to the view_autocomplete
		self.codebuff = GtkSource.Buffer()
		self.codebuff.begin_not_undoable_action()
		self.codebuff.set_text(self.codelist)
		self.codebuff.end_not_undoable_action()
		self.view_codecomplete = GtkSource.CompletionWords.new('codelist')
		self.view_codecomplete.register(self.codebuff)
		self.view_completion.add_provider(self.view_codecomplete)
		#self.view_completion.connect('populate-context', self.codecomplete)
		return

	def codecomplete(self, completion_object, completion_context):
		"""
		When the signal from the completation occurs requesting for compeltions
		this will add it to the list. maybe someday, currently broke, connect commented out
		"""
		view_code_proposal = GtkSource.CompletionProposal
		view_code_proposal.equal(view_code_proposal, 1)
		completion_context.add_proposals(self.view_codecomplete, view_code_proposal, 'test')
		return

def main():
	gui = Simple_Program()
	gui.show()
	Gtk.main()

if __name__ == '__main__':
	main()

