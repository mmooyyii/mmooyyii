.global _start

_start:
	movl $22, 	%eax
    movl $1,   %edx
    addl %edx,  %eax
    call _exit

_exit:
    movl %eax,%ebx   # exit_code
    movl $1,%eax     # 系统调用号(sys_exit)    
    int  $0x80       # 调用内核功能
