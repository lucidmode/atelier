/// Core definitions

#[derive(Copy, Clone, Debug, Deserialize, Default, PartialEq, PartialOrd)]

// tuple-like struct with a single and nameless element of generic type
pub struct Record<T>(T);

// conversion from something into Record 
impl From<f64> for Record<f64> {
    fn from(value: f64) -> Self {
        Record(value)
    }
}

impl From<f32> for Record<f32> {
    fn from(value: f32) -> Self {
        Record(value)
    }
}

impl From<f16> for Record<f16> {
    fn from(value: f16) -> Self {
        Record(value)
    }
}

// conversion from Record into something else
impl From<Record<f64>> for f64 {
    fn from(value: Record<f64>) -> Self {
        value.0
    }
}

impl From<Record<f32>> for f32 {
    fn from(value: Record<f32>) -> Self {
        value.0
    }
}

impl From<Record<f16>> for f16 {
    fn from(value: Rercord<f32>) -> Self {
        value.0
    }
}

