#!/usr/bin/env python3

# Filename: edgedetect.py
# Author: Oscar Gonzalez Cambronero
# Created: 2025-09-10
# Description: This script processes an input image file, applies an edge detection filter using GStreamer and outputs it using jpg format adding the name suffix _edges.

import sys
import os
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

def main():
    if len(sys.argv) != 2:
        print("How to Use: python3 edgedetect.py <input_image>")
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)

    #Set output file name
    name, ext = os.path.splitext(input_file)
    output_file = f"{name}_edges{ext}"

    Gst.init(None)

    #Create pipeline and elements
    pipeline = Gst.Pipeline.new("image-processor")

    filesrc = Gst.ElementFactory.make("filesrc", "source")
    decodebin = Gst.ElementFactory.make("decodebin", "decoder")
    videoconvert1 = Gst.ElementFactory.make("videoconvert", "convert1")
    edgedetector = Gst.ElementFactory.make("edgedetect", "edgedetector")
    videoconvert2 = Gst.ElementFactory.make("videoconvert", "convert2")
    pngenc = Gst.ElementFactory.make("pngenc", "encoder")
    filesink = Gst.ElementFactory.make("filesink", "sink")

    if not all([filesrc, decodebin, videoconvert1, edgedetector, videoconvert2, pngenc, filesink]):
        print("Failed to create GStreamer elements")
        sys.exit(1)

    #Set properties for input and output sources/sinks
    filesrc.set_property("location", input_file)
    filesink.set_property("location", output_file)

    #Add elements to pipeline
    pipeline.add(filesrc)
    pipeline.add(decodebin)
    pipeline.add(videoconvert1)
    pipeline.add(edgedetector)
    pipeline.add(videoconvert2)
    pipeline.add(pngenc)
    pipeline.add(filesink)

    #Link elements except decodebin
    filesrc.link(decodebin)
    videoconvert1.link(edgedetector)
    edgedetector.link(videoconvert2)
    videoconvert2.link(pngenc)
    pngenc.link(filesink)

    #Dynamic link path for decodebin
    def on_pad_added(element, pad):
        caps = pad.get_current_caps()
        if caps:
            structure_name = caps.get_structure(0).get_name()
            print(f"New pad with caps: {structure_name}")

            if structure_name.startswith("video/"):
                sink_pad = videoconvert1.get_static_pad("sink")
                if not sink_pad.is_linked():
                    link_result = pad.link(sink_pad)
                    if link_result != Gst.PadLinkReturn.OK:
                        print(f"Failed to link pads: {link_result}")
                    else:
                        print("Successfully linked decodebin to videoconvert1, media type inferred")

    decodebin.connect("pad-added", on_pad_added)

    #Handles messages from a bus
    bus = pipeline.get_bus()
    bus.add_signal_watch()

    def on_message(bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            print(f"Successfully processed image: {output_file}")
            loop.quit()
        elif t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print(f"Error found: {err}")
            print(f"Debug info: {debug}")
            loop.quit()
        elif t == Gst.MessageType.WARNING:
            warn, debug = message.parse_warning()
            print(f"Warning: {warn}")
            print(f"Debug info: {debug}")

    bus.connect("message", on_message)

    #Test if the pipeline works and start processing
    ret = pipeline.set_state(Gst.State.PLAYING)
    if ret == Gst.StateChangeReturn.FAILURE:
        print("Failed to start pipeline")
        sys.exit(1)

    loop = GLib.MainLoop()

    try:
        loop.run()
    except KeyboardInterrupt:
        print("\nInterrupted by Ctrl+C")
    finally:
        pipeline.set_state(Gst.State.NULL)

if __name__ == "__main__":
    main()