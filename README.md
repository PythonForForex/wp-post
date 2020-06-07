# wp-post

This script automatically submits posts to WordPress websites using selenium.

There is an example that uses PyDocX to grab the contents from a Word doc file and post the contents from it to WP. Another method is to use Win32Clipboard to copy the contents into the clipboard and then have that read into the script.




ToDO

- Improve usage of WP modals when uploading images. (Once one image is uploaded, WP opens a new modal for subsequent images). A cleaner way to do this is to grab the parent div ID of the active modal before starting the upload image process.
- Use selenium methods rather than the sleep function
- Implement JavaScript functions for ReadyState / verify that the page has loaded rather than use sleep function