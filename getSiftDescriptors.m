% Get list of all other image files
d = dir(fullfile('../data_pngs','JPC*.png'));

Nimages = numel(d);

for j = 1 : Nimages
	[image, descriptors, locs] = sift(fullfile('../data_pngs',d(j).name));
	siftout = [descriptors locs];
	filename = fullfile('../descriptions',d(j).name);
	csvwrite(filename,siftout);
end
