<<<<<<< HEAD
fn main() {
    // Basic print
    println!("atelier");
    
=======
use pyo3::prelude::*;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn atelier_sum(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    Ok(())
>>>>>>> e7aa7014d03398b389ac1d29fae5a8856299f3ca
}
