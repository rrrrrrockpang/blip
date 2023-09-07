import "./FilterDropdown.css";

const boldFirstLetter = (text) => {
    return text.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
};

function FilterDropdown({ label, options, onChange }) {
  return (
      <div className="form-group dropdown">
          <label htmlFor={`filter-${label}`} className="sr-only">{label}</label>
          <div className="input-group">
              {/* <label className="input-group-prepend"> */}
                  <label className="input-group-text">{label}</label>
              {/* </label> */}
              <select 
                  className="custom-select form-select" 
                  id={`filter-${label}`}
                  onChange={(e) => onChange(e.target.value)}
              >
                  <option value="">All</option>
                  {options.map((option, index) => (
                      <option key={index} value={option}>{boldFirstLetter(option)}</option>
                  ))}
              </select>
          </div>
      </div>
  );
}

export default FilterDropdown;