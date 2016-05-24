<?php
$command = "python ../vulscan/vulscan.py www.baidu.com --verify website file 10 5";
exec("pwd", $a, $b);
exec($command, $out, $status);
echo $a[0].$b.$out[0].$status;
?>