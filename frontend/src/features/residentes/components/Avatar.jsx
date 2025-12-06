import { getInitials } from "../utils/getInitials";
import { getColorFromString } from "../utils/getColorFromString";

export default function Avatar({ name, size = 48 }) {
    const initials = getInitials(name);
    const bgColor = getColorFromString(name);

    return (
        <div
            className="flex items-center justify-center rounded-full text-white font-bold"
            style={{
                width: size,
                height: size,
                backgroundColor: bgColor,
                fontSize: size * 0.4,
            }}
        >
            {initials}
        </div>
    );
}
