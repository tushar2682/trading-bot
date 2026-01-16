import React, { useRef, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Float, Sphere, MeshDistortMaterial } from '@react-three/drei';
import * as THREE from 'three';

const ParticleField = ({ count = 2000 }) => {
    const points = useMemo(() => {
        const p = new Float32Array(count * 3);
        for (let i = 0; i < count; i++) {
            p[i * 3] = (Math.random() - 0.5) * 10;
            p[i * 3 + 1] = (Math.random() - 0.5) * 10;
            p[i * 3 + 2] = (Math.random() - 0.5) * 10;
        }
        return p;
    }, [count]);

    const pointsRef = useRef();

    useFrame((state) => {
        pointsRef.current.rotation.y += 0.001;
        pointsRef.current.rotation.x += 0.0005;
    });

    return (
        <points ref={pointsRef}>
            <bufferGeometry>
                <bufferAttribute
                    attach="attributes-position"
                    count={count}
                    array={points}
                    itemSize={3}
                />
            </bufferGeometry>
            <pointsMaterial
                size={0.015}
                color="#0A84FF"
                transparent
                opacity={0.4}
                sizeAttenuation
            />
        </points>
    );
};

const AmbientShape = () => {
    return (
        <Float speed={2} rotationIntensity={1} floatIntensity={2}>
            <Sphere args={[1, 100, 100]} scale={1.5}>
                <MeshDistortMaterial
                    color="#1c1c1e"
                    attach="material"
                    distort={0.4}
                    speed={1.5}
                    roughness={0}
                    transparent
                    opacity={0.1}
                />
            </Sphere>
        </Float>
    );
};

const ThreeVisualizer = () => {
    return (
        <div id="three-canvas-container">
            <Canvas camera={{ position: [0, 0, 5], fov: 75 }}>
                <ambientLight intensity={0.5} />
                <pointLight position={[10, 10, 10]} intensity={1} color="#0A84FF" />
                <ParticleField />
                <AmbientShape />
            </Canvas>
        </div>
    );
};

export default ThreeVisualizer;
