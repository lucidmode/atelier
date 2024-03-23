/// An atomic data point

#[derive(Copy, Clone, Debug, Deserialize, Default, PartialEq, PartialOrd)]

// tuple-like struct with a single and nameless element of generic type
pub struct Record<T>(T);


