## Design Principles

### Atomic elements

- Record:  

### Axis: A collection of n atomic elements

- Vector of Records: Variable size, same data type, it can change at run time.
- Array of Records: Fixed size,  determined at compile time.

- Rule of reference: 
    - A one-to-one connection between an atomic element and a metadata object
    - A one-to-many connection among a collection of elements and 
- Rule of sequence: 
    - Equally distributed in a collection
    - Un-equally distributed in a collection

- Rule of type: 
    - Same datatype in the collection
    - Different datatype in the collection

- Rule of composition: 
    - One object can contain other objects
    - The depth of composition is dictated by the rule of reference

