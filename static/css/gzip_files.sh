#!/bin/bash
cp style.css style_orig.css
gzip -9 style.css
mv style_orig.css style.css
