var x = 5;
console.log(x);

function testOne() {
    x = x + 10;
    var y = 3;
    console.log(x);
    // console.log(y);
}
testOne();
console.log(x);
console.log(y);