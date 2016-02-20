dir1 = "C:\\Users\\Printer\\Desktop\\mhacksrefactor\\All247images\\All247images\\";
dir2 = "C:\\Users\\Printer\\Desktop\\mhacksrefactor\\All247images\\pngimgs\\";
list = getFileList(dir1);
setBatchMode(true);
for (i=0; i<list.length; i++) {
	showProgress(i+1, list.length);
	filename = dir1 + list[i];
	str = "open=" + filename + " image=[16-bit Unsigned] width=2048 height=2048 offset=0 number=1 gap=0 white";
	run("Raw...", str);
	saveAs("png", dir2+list[i]);
	close();
}
