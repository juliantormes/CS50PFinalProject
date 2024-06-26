import React from 'react';
import PropTypes from 'prop-types';

const Error = ({ message }) => <div>Error loading data: {message}</div>;

Error.propTypes = {
  message: PropTypes.string.isRequired,
};

export default Error;
