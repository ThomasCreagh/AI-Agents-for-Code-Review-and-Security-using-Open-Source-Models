"use client";

import React, { useRef, useEffect } from "react";

interface Particle {
  x: number;
  y: number;
  size: number;
  speedX: number;
  speedY: number;
  color: string;

  update(canvas: HTMLCanvasElement): void;
  draw(ctx: CanvasRenderingContext2D): void;
}

class ParticleImpl implements Particle {
  x: number;
  y: number;
  size: number;
  speedX: number;
  speedY: number;
  color: string;

  constructor(canvas: HTMLCanvasElement) {
    this.x = Math.random() * canvas.width;
    this.y = Math.random() * canvas.height;
    this.size = Math.random() * 3 + 1;
    this.speedX = (Math.random() - 0.5) * 0.5;
    this.speedY = (Math.random() - 0.5) * 0.5;
    this.color = "#0f62fe";
  }

  update(canvas: HTMLCanvasElement) {
    this.x += this.speedX;
    this.y += this.speedY;
    if (this.x > canvas.width) this.x = 0;
    else if (this.x < 0) this.x = canvas.width;
    if (this.y > canvas.height) this.y = 0;
    else if (this.y < 0) this.y = canvas.height;
  }

  draw(ctx: CanvasRenderingContext2D) {
    ctx.fillStyle = this.color;
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
    ctx.fill();
  }
}

const ParticleCanvas: React.FC<{ particleCount?: number }> = ({
  particleCount = 50,
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const setCanvasDimensions = () => {
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
    };

    setCanvasDimensions();
    window.addEventListener("resize", setCanvasDimensions);

    const particles: Particle[] = [];
    for (let i = 0; i < particleCount; i++) {
      particles.push(new ParticleImpl(canvas));
    }

    function animate() {
      if (ctx && canvas) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        for (const particle of particles) {
          particle.update(canvas);
          particle.draw(ctx);
        }
        requestAnimationFrame(animate);
      }
    }

    animate();

    return () => {
      window.removeEventListener("resize", setCanvasDimensions);
    };
  }, [particleCount]);

  return (
    <canvas
      ref={canvasRef}
      className="absolute inset-0 w-full h-full -z-5 opacity-70 pointer-events-none"
    />
  );
};

export default ParticleCanvas;
