import React, { useEffect, useState } from 'react';
import { Row, Col } from 'antd';
// import 'antd/dist/antd.css';
import './App.css';

import { BorderOutlined, UserOutlined } from '@ant-design/icons';

// Example 4x4 array representing values (0 or 1)

function App() {
  const [valueArray, setValueArray] = useState([
    [0, 1, 0, 1],
    [1, 0, 1, 0],
    [0, 1, 0, 1],
    [1, 0, 1, 0]
  ]);

  // Function to update valueArray with random values (0 or 1)
  const updateValueArray = () => {
    const newArray = valueArray.map((row: number[]) =>
      row.map(() => Math.random() > 0.5 ? 1 : 0)
    );
    setValueArray(newArray);
  };

  // Run updateValueArray function every 2 seconds
  useEffect(() => {
    const interval = setInterval(updateValueArray, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="container">
      {valueArray.map(function(row : number[]){
        return <Row gutter={8}>
          {row.map(function(v){
            if (v === 0) return <Col span={6} offset={0}><EmptyIcon size={64}/></Col>
            else return <Col span={6} offset={0}><AimIcon size={64}/></Col>
          })}
        </Row>
      })}
    </div>
  );
}

const AimIcon = ({ size }: { size: number }) => {
  return <UserOutlined style={{ fontSize: size , borderRadius:10,backgroundColor:"#FFFFFF"}} />;
};
const EmptyIcon = ({ size}: { size: number }) => {
  return <BorderOutlined style={{ fontSize: size }} />;
};


export default App;
