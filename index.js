
function main() {
    pi = Math.PI;
    let ax = 0;
    let bx = 0;
    ax = pi;
    ax /= 4;
    ax = Math.ctg(ax);
    console.log(ax);
    bx = pi;
    bx *= 5;
    bx /= 3;
    bx = Math.cos(bx);
    console.log(bx);
    ax += bx;
    console.log(ax);
}

Math.ctg = (x) => {
    return 1 / Math.tan(x)
}

main();