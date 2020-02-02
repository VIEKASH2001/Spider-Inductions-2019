const int columnPins[] = {8,9,10,11,12};// columns of the array are connected here
const int rowPins[] = {3, 4, 5, 6, 7}; // rows of the array are connected here
int image[5][5];//the numpy array will be recreated in this array
int pixel;//stores the value of 0 or 1 according to the value in a particular position of image array
int column_index;//variable for column index of image array, used in recreation and displaying loops
int row_index;//variable for row index of image array, used in recreation and displaying loops
long int pydata;//the decimal number sent from python is recived and stored in this variable

void setup() {
Serial.begin(9600);
for (int i = 0; i < 5; i++)
{
 pinMode(rowPins[i], OUTPUT); // make all the LED pins outputs
 pinMode(columnPins[i], OUTPUT);// make all the LED pins outputs
 digitalWrite(columnPins[i], HIGH); // disconnect column pins from Ground
}
//to recive data from python
while (Serial.available() == 0) {}
pydata = Serial.parseInt();
}
  
void loop()
{
  
//to recreate the numpy array by doing decimal to binary conversion
//recreation loops
  for(row_index=0;row_index<5;row_index++) 
  {
   for(column_index=0;column_index<5;column_index++)
   {
    image[row_index][column_index]=pydata%2;
    pydata/=2;
   }
  }
  
//displaying the numpy array 
//displaying loops 
  for(row_index=4;row_index>=0;row_index--) 
  {
   for(column_index=4;column_index>=0;column_index--)
   {
    Serial.print(image[row_index][column_index]);
    Serial.print("\t");
   }
   Serial.print("\n");
  }
  
//loop to glow LEDs.Positions with 1 will be the places where LEds will glow.  
  for(int row = 4; row >= 0; row--)
  {
   digitalWrite(rowPins[row], HIGH);
   for(int column = 4; column >=0; column--)
   {
    pixel = image[row][column];
    if(pixel == 1)
     digitalWrite(columnPins[column], LOW);
    delayMicroseconds(50);
    digitalWrite(columnPins[column], HIGH);  
   }
   digitalWrite(rowPins[row], LOW);
  }
}
