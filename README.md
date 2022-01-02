# What is it?

This is language, which has assembly like syntax and need to do use math
Compiles to javascript file

# Responsibility

Tu use it, you must have:
- python 3.x and above
- node js 14.x and above

# Examples

### $$ 1 + 2 $$

```nasm
START:

.main
    use ax, bx

    mov ax, 1
    mov bx, 2

    add ax, bx

    syscall 1x00, ax

END
```

Result: $$ 3 $$

### $$ ctg \frac{\pi}{4} + sin \frac{5\pi}{3}$$

```nasm
START:

.main
    use ax, bx

    stp ax
    div ax, 4
    ctg ax

    stp bx
    sub bx, 5
    div bx, 3
    cos bx

    add ax, bx

    syscall 1x00, ax
    
END
```

Result: $$ 1.5 $$
