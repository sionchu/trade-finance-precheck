import type { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import { ChartNoAxesCombined, FileText, Settings2 } from "lucide-react";
import { motion, MotionConfig } from "motion/react";
import { useEffect, useState, type ComponentType, type ReactElement } from "react";

export type ViewId = "setup" | "analysis" | "report";
type View = { id: ViewId; label: string };
export type ExperienceData = { views: View[]; activeView: ViewId };
export type ExperienceState = { active_view: ViewId };
type Tools = Pick<FrontendRendererArgs<ExperienceState, ExperienceData>, "setStateValue">;
const icons: Record<ViewId, ComponentType<{ size?: number; "aria-hidden"?: boolean }>> = {
  setup: Settings2, analysis: ChartNoAxesCombined, report: FileText,
};
export default function ExperienceShell({ data, setStateValue }: Tools & { data: ExperienceData }): ReactElement {
  const [activeView, setActiveView] = useState<ViewId>(data.activeView);
  useEffect(() => setActiveView(data.activeView), [data.activeView]);
  return <MotionConfig reducedMotion="user" transition={{ duration: 0.18 }}>
    <nav className="views" aria-label="금융진단 화면">
      {data.views.map(view => {
        const Icon = icons[view.id];
        const selected = activeView === view.id;
        return <button className="view" type="button" key={view.id}
          aria-current={selected ? "page" : undefined}
          onClick={() => { setActiveView(view.id); setStateValue("active_view", view.id); }}>
          <Icon size={19} aria-hidden /><span>{view.label}</span>
          {selected && <motion.span className="view-indicator" layoutId="view-indicator" />}
        </button>;
      })}
    </nav>
  </MotionConfig>;
}
