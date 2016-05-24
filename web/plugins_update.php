<?php
require_once('common.php');
?>

<?php
//	check login first
if (!already_login()) {
    die();
}
?>

<?php
$command = "python ../vulscan/Pocsuite/pocsuite/tests/update.py";
system($command, $return_var);
if($return_var == 0) {
    echo "<script>alert('update plugins successful !');window.location.href='http://localhost/ICSScan/web/plugins.php';</script>";
}
else {
    echo "<script>alert('update plugins failed !');window.location.href=\'http://localhost/ICSScan/web/plugins.php\';</script>";
}
?>