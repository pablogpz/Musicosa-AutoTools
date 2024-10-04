$VideoclipFilename = "video.mp4"
$TemplateFilename = "image.png"
$VideoOutFilename = "out.mp4"

$VideoclipTimestampStart = "00:00"
$VideoclipTimestampEnd = "00:30"
$VideoclipWScale = 1080
$videoclipPositionTop = 86
$videoclipPositionLeft = 756

$targetFps = 30

ffmpeg -ss $VideoclipTimestampStart -to $VideoclipTimestampEnd -i $VideoclipFilename -i $TemplateFilename `
-filter_complex "[0:v]scale=$($VideoclipWScale):-1[v0scaled];[1][v0scaled]overlay=x=$($videoclipPositionLeft):y=$($videoclipPositionTop)" `
-r:v $targetFps -c:a copy `
-preset "slow" -tune "film" `
-y `
$VideoOutFilename