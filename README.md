# MinimalPlayer
A CLI-based player that uses FFmpeg and basic pulseaudio/pipewire tools (or ffplay specially for non-linux os) to play audio, with speed configuration.
<br>Now you might be confused: Why does this software exist in the first place?
<br>..yes
<br>
<br>Anyways short explanation; this media player basically exist, because I created it. But the particular purpose is, well, for nothing. It's just your basic music (not video) player.
<br>This media player is CLI-based, which makes life harder (or probably not, I don't know). Oh right, this enables media playing for CLI-only distros, that's the purpose
<br>There are three arguments that you either want to put within the `minimalplayer` command, such as --file (-f, the file location, obviously), --pipe (-p, if you want to pipe the raw audio output to a pipe or stdout), --speed (-s, adjusting the speed (the second purpose of this program)), and that's it. For looping, add `while true; do (the command); done`
<br>The utility supports modern oses (Linux, Windows, macOS not supported yet)
