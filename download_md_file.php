<?php
if(isset($_POST['url'])) {
  $url = $_POST['url']; // Get the URL input from the form
  $md = file_get_contents($url); // Download the file contents as a string
  header('Content-Type: application/octet-stream'); // Set the header to indicate a file download
  header('Content-Disposition: attachment; filename="'.basename($url).'.md"'); // Set the filename of the downloaded file
  echo $md; // Output the Markdown file as a file download
}
?>
