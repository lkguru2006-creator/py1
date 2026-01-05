import React from 'react';

const ThreeDLetterG = () => {
    return (
        <div className="relative w-32 h-32 preserve-3d perspective-1000 animate-float pointer-events-none select-none">
            <div className="relative w-full h-full transform-style-3d rotate-y-12 rotate-x-12">
                {/* Main G Shape - constructed from parts to simulate 3D or using a thick font with text-shadow layers */}
                {/* For a pure CSS 3D letter without importing 3D models, we use layered text-shadows or stacked elements */}

                <div className="flex items-center justify-center w-full h-full">
                    <span className="text-[10rem] font-black leading-none text-transparent bg-clip-text bg-gradient-to-br from-meta-base to-meta-light drop-shadow-2xl relative z-10"
                        style={{
                            textShadow: `
                          0px 1px 0px #004DAD,
                          1px 2px 0px #004DAD,
                          2px 3px 0px #004DAD,
                          3px 4px 0px #004DAD,
                          4px 5px 0px #004DAD,
                          5px 6px 0px #004DAD,
                          6px 7px 0px #004DAD,
                          7px 8px 7px rgba(0,0,0,0.4),
                          -1px -1px 0 rgba(255,255,255,0.2)
                      `
                        }}>
                        G
                    </span>

                    {/* Ambient Lighting/Glow */}
                    <div className="absolute inset-0 bg-blue-500/20 blur-3xl rounded-full -z-10 animate-pulse"></div>
                </div>
            </div>
        </div>
    );
};

export default ThreeDLetterG;
