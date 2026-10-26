shader_type canvas_item;
// Soft dark vignette + very light warm tint at the edges, drawn over the 3D scene (under the UI).
uniform float strength : hint_range(0.0, 1.0) = 0.55;
uniform float radius : hint_range(0.3, 1.2) = 0.78;

void fragment() {
	vec2 uv = UV * 2.0 - 1.0;
	uv.x *= 1.15;
	float d = length(uv);
	float v = smoothstep(radius, radius + 0.75, d);
	COLOR = vec4(0.03, 0.01, 0.02, v * strength);
}
