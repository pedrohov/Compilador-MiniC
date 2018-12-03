int main() {
	int x, i;
	
	i = 0;
	while(i < 10) {
		if(i > 5) {
			print(i);
			continue;
		}
		i = i + 1;
		print(i, "\n");
	}

	print(x, "\n");

	return 0;
}