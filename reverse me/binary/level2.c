#include <stdio.h>
#include <string.h>

#define test "__stack_check"
//atoi, exit, fflush, memset, strcmp, stdin, strlen, puts, 
//fonction: n, no, ok, ww, xd, xxd, xxxd, xyxxd
int main()
{
	static char buf[10];
	printf("Please enter key: ");
	scanf("%s", buf);
	if (strcmp(buf, test) == 0)
		printf("Good job.");
	else
		printf("Nope.");
}