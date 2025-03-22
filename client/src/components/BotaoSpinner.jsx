import React from "react";
import { Button, Spinner } from "react-bootstrap";

const BotaoSpinner = ({ loading, fixo, temp }) => {
  return (
    <Button
      variant="primary"
      type="submit"
      className="p-2 ms-auto"
      disabled={loading}
    >
      {loading ? (
        <>
          <Spinner
            as="span"
            animation="border"
            size="sm"
            role="status"
            aria-hidden="true"
            className="me-2"
          />
          {temp}
        </>
      ) : fixo}
    </Button>
  );
};

export default BotaoSpinner;
